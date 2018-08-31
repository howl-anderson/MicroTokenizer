#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MicroTokenizer


def test_DAG():
    result = MicroTokenizer.cut_by_DAG("他走了")

    assert result == ['他', '走', '了']


def test_HMM():
    result = MicroTokenizer.cut_by_HMM("他走了")

    assert result == ['他', '走', '了']


def test_CRF():
    result = MicroTokenizer.cut_by_CRF("他走了")

    assert result == ['他', '走', '了']


def test_max_match_forward():
    result = MicroTokenizer.cut_by_joint_model("他走了")

    assert result == ['他', '走', '了']
