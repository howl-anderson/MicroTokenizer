#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `MicroTokenizer` package."""

from MicroTokenizer.CRF.crf_tokenizer import CRFTokenizer


def test_persist(tmpdir):
    temp_path = tmpdir.mkdir("dag")

    tokenizer = CRFTokenizer()
    tokenizer.train_one_line(["我", "是", "中国人"])
    tokenizer.train_one_line(["你", "打", "人"])
    tokenizer.do_train()
    tokenizer.persist_to_dir(temp_path)

    assert len(temp_path.listdir()) == 1


def test_segment():
    tokenizer = CRFTokenizer()
    tokenizer.load_model()
    result = tokenizer.segment("你打人")

    assert result == ['你', '打人']
