# -*- coding: utf-8 -*-
"""
format_apa_docx.py
==================
Post-procesador OpenXML para asegurar que el documento Word exportado por Quarto
cumpla estrictamente las normas APA 7 / UNL con estilos dedicados para:
  - Table Number / Figure Number (10 pt, negrita, sin sangría, alineado a la izquierda)
  - Table Caption / Image Caption (10 pt, cursiva, sin sangría, alineado a la izquierda, en línea separada)
  - Table Header (10 pt, negrita, sin sangría)
  - Table Text / Compact (10 pt, sin sangría, dentro de las celdas)
  - Table Note (10 pt, sin sangría, con 'Nota.' en cursiva y el resto en redonda)
  - Bordes APA 7 (línea superior, línea bajo encabezado y línea inferior; sin bordes verticales)
  - Desempaquetado de las tablas contenedoras 1x1 de Quarto para evitar doble sangría o anidamiento
"""

import re
import shutil
from copy import deepcopy
from pathlib import Path
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


PPR_CHILD_ORDER = [
    'pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widRow',
    'numPr', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap',
    'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi',
    'adjustRightInd', 'snapToGrid', 'spacing', 'ind', 'contextSpacing',
    'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection', 'textAlignment',
    'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange'
]
_PPR_ORDER_MAP = {tag: i for i, tag in enumerate(PPR_CHILD_ORDER)}


def normalize_pPr(pPr):
    children = list(pPr)
    if not children:
        return
    children.sort(key=lambda c: _PPR_ORDER_MAP.get(c.tag.split('}')[-1], 999))
    for c in list(pPr):
        pPr.remove(c)
    for c in children:
        pPr.append(c)


def set_clean_pPr(p_elem, style_id, align=None, keep_next=False):
    # Remove all existing w:pPr (fixes Pandoc's duplicate <w:pPr> bug)
    for old_pPr in p_elem.findall(qn('w:pPr')):
        p_elem.remove(old_pPr)
    pPr = OxmlElement('w:pPr')
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), style_id)
    pPr.append(pStyle)

    if keep_next:
        pPr.append(OxmlElement('w:keepNext'))

    ind = OxmlElement('w:ind')
    ind.set(qn('w:firstLine'), '0')
    ind.set(qn('w:left'), '0')
    pPr.append(ind)

    if align:
        jc = OxmlElement('w:jc')
        jc.set(qn('w:val'), align)
        pPr.append(jc)

    normalize_pPr(pPr)
    p_elem.insert(0, pPr)


def set_apa_table_borders(tbl_elem):
    tblPr = tbl_elem.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl_elem.insert(0, tblPr)

    # Remove table indent so it aligns flush left with caption and note
    old_ind = tblPr.find(qn('w:tblInd'))
    if old_ind is not None:
        tblPr.remove(old_ind)
    tblInd = OxmlElement('w:tblInd')
    tblInd.set(qn('w:w'), '0')
    tblInd.set(qn('w:type'), 'dxa')
    tblPr.append(tblInd)

    # Set 100% width (5000 pct)
    old_w = tblPr.find(qn('w:tblW'))
    if old_w is not None:
        tblPr.remove(old_w)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)

    # Set APA 7 table borders (top and bottom horizontal lines only)
    old_bdr = tblPr.find(qn('w:tblBorders'))
    if old_bdr is not None:
        tblPr.remove(old_bdr)
    tblBorders = OxmlElement('w:tblBorders')
    for b_name, val, sz in [
        ('top', 'single', '8'),
        ('bottom', 'single', '8'),
        ('left', 'none', '0'),
        ('right', 'none', '0'),
        ('insideH', 'none', '0'),
        ('insideV', 'none', '0'),
    ]:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), val)
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), '000000')
        tblBorders.append(b)
    tblPr.append(tblBorders)


def format_inner_table(tbl_elem):
    set_apa_table_borders(tbl_elem)
    rows = tbl_elem.findall(qn('w:tr'))
    for r_idx, tr in enumerate(rows):
        is_header = (r_idx == 0)
        for tc in tr.findall(qn('w:tc')):
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is None:
                tcPr = OxmlElement('w:tcPr')
                tc.insert(0, tcPr)
            # Header row gets bottom border per APA 7
            old_tcBdr = tcPr.find(qn('w:tcBorders'))
            if old_tcBdr is not None:
                tcPr.remove(old_tcBdr)
            if is_header:
                tcBorders = OxmlElement('w:tcBorders')
                top_b = OxmlElement('w:top')
                top_b.set(qn('w:val'), 'single')
                top_b.set(qn('w:sz'), '8')
                top_b.set(qn('w:space'), '0')
                top_b.set(qn('w:color'), '000000')
                bot_b = OxmlElement('w:bottom')
                bot_b.set(qn('w:val'), 'single')
                bot_b.set(qn('w:sz'), '6')
                bot_b.set(qn('w:space'), '0')
                bot_b.set(qn('w:color'), '000000')
                tcBorders.append(top_b)
                tcBorders.append(bot_b)
                tcPr.append(tcBorders)

            for p in tc.findall(qn('w:p')):
                # Keep alignment if right/center was set by Pandoc
                existing_align = 'left'
                for pPr in p.findall(qn('w:pPr')):
                    jc = pPr.find(qn('w:jc'))
                    if jc is not None and jc.get(qn('w:val')):
                        existing_align = jc.get(qn('w:val'))
                style_to_use = 'TableHeader' if is_header else 'TableText'
                set_clean_pPr(p, style_to_use, align=existing_align, keep_next=is_header)
                # Ensure all runs in table have 10pt (20 half-points)
                for r in p.findall(qn('w:r')):
                    rPr = r.find(qn('w:rPr'))
                    if rPr is None:
                        rPr = OxmlElement('w:rPr')
                        r.insert(0, rPr)
                    for sz_tag in ['w:sz', 'w:szCs']:
                        old_sz = rPr.find(qn(sz_tag))
                        if old_sz is not None:
                            rPr.remove(old_sz)
                        new_sz = OxmlElement(sz_tag)
                        new_sz.set(qn('w:val'), '20')
                        rPr.append(new_sz)


def make_text_para(text, style_id, bold=False, italic=False, keep_next=True):
    p = OxmlElement('w:p')
    set_clean_pPr(p, style_id, align='left', keep_next=keep_next)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    if bold:
        rPr.append(OxmlElement('w:b'))
        rPr.append(OxmlElement('w:bCs'))
    if italic:
        rPr.append(OxmlElement('w:i'))
        rPr.append(OxmlElement('w:iCs'))
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '20')
    szCs = OxmlElement('w:szCs')
    szCs.set(qn('w:val'), '20')
    rPr.append(sz)
    rPr.append(szCs)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    r.append(t)
    p.append(r)
    return p


def process_docx(docx_path: Path):
    doc = docx.Document(str(docx_path))
    body = doc._element.body

    # 1. Unwrap Quarto 1x1 wrapper tables (both Table wrappers and Figure wrappers)
    for tbl in list(body.findall(qn('w:tbl'))):
        rows = tbl.findall(qn('w:tr'))
        if len(rows) == 1:
            cells = rows[0].findall(qn('w:tc'))
            if len(cells) == 1:
                tc = cells[0]
                paras = tc.findall(qn('w:p'))
                inner_tbls = tc.findall(qn('w:tbl'))
                if paras:
                    first_p_text = ''.join(t.text or '' for t in paras[0].findall('.//' + qn('w:t'))).strip()
                    # Match 'Tabla X. Title' or 'Figura X. Title'
                    m = re.match(r'^((?:Tabla|Figura)\s+\d+)\.\s*(.+)$', first_p_text, flags=re.DOTALL)
                    if m:
                        label_num = m.group(1).replace('\xa0', ' ')
                        title_str = m.group(2).strip()
                        is_table = label_num.startswith('Tabla')

                        p_num = make_text_para(label_num, 'TableNumber', bold=True, italic=False, keep_next=True)
                        p_cap = make_text_para(title_str, 'TableCaption' if is_table else 'ImageCaption',
                                               bold=False, italic=True, keep_next=True)

                        tbl.addprevious(p_num)
                        tbl.addprevious(p_cap)

                        if inner_tbls:
                            inner_tbl = deepcopy(inner_tbls[0])
                            format_inner_table(inner_tbl)
                            tbl.addprevious(inner_tbl)
                        else:
                            # It's a figure wrapper: copy the remaining paragraphs (which contain the drawing)
                            for fig_p in paras[1:]:
                                fig_p_copy = deepcopy(fig_p)
                                set_clean_pPr(fig_p_copy, 'CaptionedFigure', align='center', keep_next=False)
                                tbl.addprevious(fig_p_copy)

                        body.remove(tbl)

    # 2. Also check standalone Figure captions if any were emitted outside 1x1 tables
    for p in list(body.findall(qn('w:p'))):
        txt = ''.join(t.text or '' for t in p.findall('.//' + qn('w:t'))).strip()
        m_fig = re.match(r'^((?:Tabla|Figura)\s+\d+)\.\s*(.+)$', txt, flags=re.DOTALL)
        if m_fig:
            label_num = m_fig.group(1).replace('\xa0', ' ')
            title_str = m_fig.group(2).strip()
            p_num = make_text_para(label_num, 'TableNumber', bold=True, italic=False, keep_next=True)
            p_cap = make_text_para(title_str, 'ImageCaption', bold=False, italic=True, keep_next=True)
            p.addprevious(p_num)
            p.addprevious(p_cap)
            body.remove(p)
            continue

        # 3. Assign 'TableNote' style to all 'Nota.' paragraphs so they have 0 indent and 10pt size
        if txt.startswith('Nota.'):
            set_clean_pPr(p, 'TableNote', align='both', keep_next=False)
            for r in p.findall(qn('w:r')):
                rPr = r.find(qn('w:rPr'))
                if rPr is None:
                    rPr = OxmlElement('w:rPr')
                    r.insert(0, rPr)
                for sz_tag in ['w:sz', 'w:szCs']:
                    old_sz = rPr.find(qn(sz_tag))
                    if old_sz is not None:
                        rPr.remove(old_sz)
                    new_sz = OxmlElement(sz_tag)
                    new_sz.set(qn('w:val'), '20')
                    rPr.append(new_sz)

    # Normalize all pPr in document
    for pPr in body.iter(qn('w:pPr')):
        normalize_pPr(pPr)

    doc.save(str(docx_path))
    print(f'Formatted APA 7 styles and tables in: {docx_path}')


if __name__ == '__main__':
    site_docx = Path(r'd:\07_Ciclo\septimo_ciclo\public_investment_projects\_site\docs\vaults\proyecto-torata-el_oro\index.docx')
    vault_docx = Path(r'd:\07_Ciclo\septimo_ciclo\public_investment_projects\docs\vaults\proyecto-torata-el_oro\index.docx')
    if site_docx.exists():
        process_docx(site_docx)
        shutil.copy2(site_docx, vault_docx)
        print(f'Synced to: {vault_docx}')
    elif vault_docx.exists():
        process_docx(vault_docx)

