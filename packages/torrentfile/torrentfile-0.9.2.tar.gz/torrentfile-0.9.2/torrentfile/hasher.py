#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2021-current alexpdev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################
"""
Piece/File Hashers for Bittorrent meta file contents.
"""

import os
import logging
from hashlib import sha1, sha256  # nosec

from torrentfile.mixins import CbMixin, ProgMixin
from torrentfile.utils import next_power_2

BLOCK_SIZE = 2**14  # 16KiB
HASH_SIZE = 32

logger = logging.getLogger(__name__)


class Hasher(CbMixin, ProgMixin):
    """
    Piece hasher for Bittorrent V1 files.

    Takes a sorted list of all file paths, calculates sha1 hash
    for fixed size pieces of file data from each file
    seemlessly until the last piece which may be smaller than others.

    Parameters
    ----------
    paths : list
        List of files.
    piece_length : int
        Size of chuncks to split the data into.
    align: bool
        flag to indicate if the torrent should be piece aligned
    progress: int
        the progress mode
    progress_bar: [Optional] ProgressBar
        a progress bar object if progress mode is 2
    """

    def __init__(
        self,
        paths: list,
        piece_length: int,
        align: bool = False,
        progress: int = 1,
        progress_bar=None,
    ):
        """Generate hashes of piece length data from filelist contents."""
        self.piece_length = piece_length
        self.paths = paths
        self.align = align
        self.total = sum(os.path.getsize(i) for i in self.paths)
        self.index = 0
        self.current = open(self.paths[0], "rb")
        self.progress = progress
        self.progbar = progress_bar
        if self.progress == 1:
            file_size = os.path.getsize(self.paths[0])
            self.progbar = self.get_progress_tracker(file_size, self.paths[0])
        logger.debug("Hashing %s", str(self.paths[0]))

    def __iter__(self):
        """
        Iterate through feed pieces.

        Returns
        -------
        self : iterator
            Iterator for leaves/hash pieces.
        """
        return self

    def _handle_partial(self, arr: bytearray) -> bytearray:
        """
        Define the handling partial pieces that span 2 or more files.

        Parameters
        ----------
        arr : bytearray
            Incomplete piece containing partial data

        Returns
        -------
        digest : bytearray
            SHA1 digest of the complete piece.
        """
        if self.align:
            target = self.piece_length - len(arr)
            temp = bytearray(target)
            arr.extend(temp)
            return sha1(arr).digest()  # nosec

        while len(arr) < self.piece_length and self.next_file():
            target = self.piece_length - len(arr)
            temp = bytearray(target)
            size = self.current.readinto(temp)
            self.progbar.update(size)
            arr.extend(temp[:size])
            if size == target:
                break
        return sha1(arr).digest()  # nosec

    def next_file(self) -> bool:
        """
        Seemlessly transition to next file in file list.

        Returns
        -------
        bool:
            True if there is a next file otherwise False.
        """
        self.index += 1
        if self.progress == 1:
            self.progbar.close_out()
        if self.index < len(self.paths):
            path = self.paths[self.index]
            if self.progress == 1:
                total = os.path.getsize(path)
                self.progbar = self.get_progress_tracker(total, path)
            logger.debug("Hashing %s", str(path))
            self.current.close()
            self.current = open(path, "rb")
            return True
        return False

    def __next__(self) -> bytes:
        """
        Generate piece-length pieces of data from input file list.

        Returns
        -------
        bytes
            SHA1 hash of the piece extracted.
        """
        while True:
            piece = bytearray(self.piece_length)
            size = self.current.readinto(piece)
            self.progbar.update(size)
            if size == 0:
                if not self.next_file():
                    raise StopIteration
            elif size < self.piece_length:
                return self._handle_partial(piece[:size])
            else:
                return sha1(piece).digest()  # nosec


def merkle_root(blocks: list) -> bytes:
    """
    Calculate the merkle root for a seq of sha256 hash digests.

    Parameters
    ----------
    blocks : list
        a sequence of sha256 layer hashes.

    Returns
    -------
    bytes
        the sha256 root hash of the merkle tree.
    """
    if blocks:
        while len(blocks) > 1:
            blocks = [
                sha256(x + y).digest() for x, y in zip(*[iter(blocks)] * 2)
            ]
        return blocks[0]
    return blocks


class HasherV2(CbMixin, ProgMixin):
    """
    Calculate the root hash and piece layers for file contents.

    Iterates over 16KiB blocks of data from given file, hashes the data,
    then creates a hash tree from the individual block hashes until size of
    hashed data equals the piece-length.  Then continues the hash tree until
    root hash is calculated.

    Parameters
    ----------
    path : str
        Path to file.
    piece_length : int
        Size of layer hashes pieces.
    progress: int
        the progress mode
    progress_bar: [Optional] ProgressBar
        a progress bar object if progress mode is 2
    """

    def __init__(
        self,
        path: str,
        piece_length: int,
        progress: int = 1,
        progress_bar=None,
    ):
        """
        Calculate and store hash information for specific file.
        """
        self.path = path
        self.root = None
        self.piece_layer = None
        self.layer_hashes = []
        self.piece_length = piece_length
        self.num_blocks = piece_length // BLOCK_SIZE
        self.progress = progress
        self.progbar = progress_bar
        if self.progress == 1:
            size = os.path.getsize(self.path)
            self.progbar = self.get_progress_tracker(size, self.path)
        with open(self.path, "rb") as fd:
            self.process_file(fd)

    def process_file(self, fd: str):
        """
        Calculate hashes over 16KiB chuncks of file content.

        Parameters
        ----------
        fd : BytesIO
            Opened file in read mode.
        """
        while True:
            blocks = []
            leaf = bytearray(BLOCK_SIZE)
            # generate leaves of merkle tree

            for _ in range(self.num_blocks):
                size = fd.readinto(leaf)
                if not size:
                    break
                self.progbar.update(size)
                blocks.append(sha256(leaf[:size]).digest())

            # blocks is empty mean eof
            if not blocks:
                break
            if len(blocks) != self.num_blocks:
                # when size of file doesn't fill the last block
                # when the file contains multiple pieces
                remaining = self.num_blocks - len(blocks)
                if not self.layer_hashes:
                    # when the there is only one block for file
                    power2 = next_power_2(len(blocks))
                    remaining = power2 - len(blocks)

                # pad the the rest with zeroes to fill remaining space.
                padding = [bytes(32) for _ in range(remaining)]
                blocks.extend(padding)
            # calculate the root hash for the merkle tree up to piece-length

            layer_hash = merkle_root(blocks)
            self.cb(layer_hash)
            self.layer_hashes.append(layer_hash)
        if self.progress == 1:
            self.progbar.close_out()
        self._calculate_root()

    def _calculate_root(self):
        """
        Calculate root hash for the target file.
        """
        self.piece_layer = b"".join(self.layer_hashes)
        hashes = len(self.layer_hashes)
        if hashes > 1:
            pow2 = next_power_2(hashes)
            remainder = pow2 - hashes
            pad_piece = [bytes(HASH_SIZE) for _ in range(self.num_blocks)]
            for _ in range(remainder):
                self.layer_hashes.append(merkle_root(pad_piece))
        self.root = merkle_root(self.layer_hashes)


class HasherHybrid(CbMixin, ProgMixin):
    """
    Calculate root and piece hashes for creating hybrid torrent file.

    Create merkle tree layers from sha256 hashed 16KiB blocks of contents.
    With a branching factor of 2, merge layer hashes until blocks equal
    piece_length bytes for the piece layer, and then the root hash.

    Parameters
    ----------
    path : str
        path to target file.
    piece_length : int
        piece length for data chunks.
    progress: int
        the progress mode
    progress_bar: [Optional] ProgressBar
        a progress bar object if progress mode is 2
    """

    def __init__(
        self,
        path: str,
        piece_length: int,
        progress: int = 1,
        progress_bar=None,
    ):
        """
        Construct Hasher class instances for each file in torrent.
        """
        self.path = path
        self.piece_length = piece_length
        self.pieces = []
        self.layer_hashes = []
        self.piece_layer = None
        self.root = None
        self.padding_piece = None
        self.padding_file = None
        self.amount = piece_length // BLOCK_SIZE
        self.progress = progress
        self.progbar = progress_bar
        if self.progress == 1:
            size = os.path.getsize(self.path)
            self.progbar = self.get_progress_tracker(size, self.path)
        with open(path, "rb") as data:
            self.process_file(data)

    def _pad_remaining(self, block_count: int):
        """
        Generate Hash sized, 0 filled bytes for padding.

        Parameters
        ----------
        block_count : int
            current total number of blocks collected.

        Returns
        -------
        padding : bytes
            Padding to fill remaining portion of tree.
        """
        # when the there is only one block for file
        remaining = self.amount - block_count
        if not self.layer_hashes:
            power2 = next_power_2(block_count)
            remaining = power2 - block_count
        return [bytes(HASH_SIZE) for _ in range(remaining)]

    def process_file(self, data: bytearray):
        """
        Calculate layer hashes for contents of file.

        Parameters
        ----------
        data : BytesIO
            File opened in read mode.
        """
        while True:
            plength = self.piece_length
            blocks = []
            piece = sha1()  # nosec
            total = 0
            block = bytearray(BLOCK_SIZE)
            for _ in range(self.amount):
                size = data.readinto(block)
                self.progbar.update(size)
                if not size:
                    break
                total += size
                plength -= size
                blocks.append(sha256(block[:size]).digest())
                piece.update(block[:size])
            if not blocks:
                break
            if len(blocks) != self.amount:
                padding = self._pad_remaining(len(blocks))
                blocks.extend(padding)
            layer_hash = merkle_root(blocks)
            self.cb(layer_hash)
            self.layer_hashes.append(layer_hash)
            if plength > 0:
                self.padding_file = {
                    "attr": "p",
                    "length": plength,
                    "path": [".pad", str(plength)],
                }
                piece.update(bytes(plength))
            self.pieces.append(piece.digest())  # nosec
        if self.progress == 1:
            self.progbar.close_out()
        self._calculate_root()

    def _calculate_root(self):
        """
        Calculate the root hash for opened file.

        **DEPRECATED**
        """
        self.piece_layer = b"".join(self.layer_hashes)

        if len(self.layer_hashes) > 1:
            pad_piece = merkle_root([bytes(32) for _ in range(self.amount)])

            pow2 = next_power_2(len(self.layer_hashes))
            remainder = pow2 - len(self.layer_hashes)

            self.layer_hashes += [pad_piece for _ in range(remainder)]
        self.root = merkle_root(self.layer_hashes)


class FileHasher(CbMixin, ProgMixin):
    """
    Calculate root and piece hashes for creating hybrid torrent file.

    Create merkle tree layers from sha256 hashed 16KiB blocks of contents.
    With a branching factor of 2, merge layer hashes until blocks equal
    piece_length bytes for the piece layer, and then the root hash.

    Parameters
    ----------
    path : str
        path to target file.
    piece_length : int
        piece length for data chunks.
    hybrid : bool
        flag to indicate if it's a hybrid torrent
    progress: int
        the progress mode
    progress_bar: [Optional] ProgressBar
        a progress bar object if progress mode is 2
    """

    def __init__(
        self,
        path: str,
        piece_length: int,
        progress: int = 1,
        hybrid: bool = False,
        progress_bar=None,
    ):
        """
        Construct Hasher class instances for each file in torrent.
        """
        self.path = path
        self.piece_length = piece_length
        self.pieces = []
        self.layer_hashes = []
        self.piece_layer = None
        self.root = None
        self.padding_piece = None
        self.padding_file = None
        self.amount = piece_length // BLOCK_SIZE
        self.end = False
        self.progress = progress
        self.progbar = progress_bar
        if self.progress == 1:
            size = os.path.getsize(self.path)
            self.progbar = self.get_progress_tracker(size, self.path)
        self.current = open(path, "rb")
        self.hybrid = hybrid

    def __iter__(self):
        """Return `self`: needed to implement iterator implementation."""
        return self

    def _pad_remaining(self, block_count: int):
        """
        Generate Hash sized, 0 filled bytes for padding.

        Parameters
        ----------
        block_count : int
            current total number of blocks collected.

        Returns
        -------
        padding : bytes
            Padding to fill remaining portion of tree.
        """
        # when the there is only one block for file
        remaining = self.amount - block_count
        if not self.layer_hashes:
            power2 = next_power_2(block_count)
            remaining = power2 - block_count
        return [bytes(HASH_SIZE) for _ in range(remaining)]

    def __next__(self) -> bytes:
        """
        Calculate layer hashes for contents of file.

        Returns
        -------
        bytes
            The layer merckle root hash.

        Raises
        ------
        StopIteration
            Halts the iterator from progressing
        """
        if self.end:
            self.end = False
            raise StopIteration
        plength = self.piece_length
        blocks = []
        piece = sha1()  # nosec
        total = 0
        block = bytearray(BLOCK_SIZE)
        for _ in range(self.amount):
            size = self.current.readinto(block)
            self.progbar.update(size)
            if not size:
                self.end = True
                break
            total += size
            plength -= size
            blocks.append(sha256(block[:size]).digest())
            if self.hybrid:
                piece.update(block[:size])
        if not blocks:
            self._calculate_root()
            raise StopIteration
        if len(blocks) != self.amount:
            padding = self._pad_remaining(len(blocks))
            blocks.extend(padding)
        layer_hash = merkle_root(blocks)
        self.layer_hashes.append(layer_hash)
        self.cb(layer_hash)
        if self.end:
            if self.progress == 1:
                self.progbar.close_out()
            self._calculate_root()
        if self.hybrid:
            if plength > 0:
                self.padding_file = {
                    "attr": "p",
                    "length": plength,
                    "path": [".pad", str(plength)],
                }
                piece.update(bytes(plength))
            piece = piece.digest()
            self.pieces.append(piece)
            return layer_hash, piece
        return layer_hash

    def _calculate_root(self):
        """
        Calculate the root hash for opened file.
        """
        self.piece_layer = b"".join(self.layer_hashes)

        if len(self.layer_hashes) > 1:
            pad_piece = merkle_root([bytes(32) for _ in range(self.amount)])

            pow2 = next_power_2(len(self.layer_hashes))
            remainder = pow2 - len(self.layer_hashes)

            self.layer_hashes += [pad_piece for _ in range(remainder)]
        self.root = merkle_root(self.layer_hashes)
        self.current.close()
