#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MicroTokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer()


def test_DAG():
    result = tokenizer.cut_by_DAG("他走了")

    assert result == ['他', '走', '了']


def test_HMM():
    result = tokenizer.cut_by_HMM("他走了")

    assert result == ['他', '走', '了']


def test_CRF():
    result = tokenizer.cut_by_CRF("他走了")

    assert result == ['他', '走', '了']


def test_max_match_forward():
    result = tokenizer.cut_by_max_match_forward("他走了")

    assert result == ['他', '走', '了']


def test_max_match_backward():
    result = tokenizer.cut_by_max_match_backward("他走了")

    assert result == ['他', '走', '了']


def test_max_match_bidirectional():
    result = tokenizer.cut_by_max_match_bidirectional("他走了")

    assert result == ['他', '走', '了']
