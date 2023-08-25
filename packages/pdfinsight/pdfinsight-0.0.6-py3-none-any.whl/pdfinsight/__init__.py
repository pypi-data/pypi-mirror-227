import math
import re

import fitz
import pandas as pd

# extract text and coordinate information from pdf to dataframe
def pdf2df(path, precision_dp, toc_pages):
    doc = fitz.open(path)
    filename = path.split("\\")[-1]

    # we extract all the page dict into a single dict
    block_dict = {}
    page_num = 1
    for page in doc:  # Iterate all pages in the document
        file_dict = page.get_text("dict")  # Get the page dictionary
        block = file_dict["blocks"]  # Get the block information
        block_dict[page_num] = block  # Store in block dictionary
        page_num += 1  # Increase the page value by 1

    # declare empty dictionary to hold dataframe value
    df = {
        "file":[],
        "page": [],
        "block": [],
        "xmin": [],
        "ymin": [],
        "xmax": [],
        "ymax": [],
        "text": [],
        "font_size": [],
        "font_characteristics": [],
        "font": [],
        "font_color": [],
        "image": [],
    }

    # loop through each page
    for page in block_dict:
        block_num = 1
        # loop through each block in each page (1 paragrapgh is normally detected as 1 block)
        # we are only in the lines data within each block. We ignore the type, bbox and block count
        for block in block_dict[page]:
            # skip if the block is a image
            if block["type"] == 1:
                df['file'].append(filename)
                df["page"].append(page)
                df["block"].append(block_num)
                df["xmin"].append(block["bbox"][0])
                df["ymin"].append(block["bbox"][1])
                df["xmax"].append(block["bbox"][2])
                df["ymax"].append(block["bbox"][3])
                df["text"].append("")
                df["font_size"].append(0.0)
                df["font_characteristics"].append("")
                df["font"].append("")
                df["font_color"].append("")
                df["image"].append(block["image"])
            else:
                # loop through each line of each block
                for line in block["lines"]:
                    # for each line, only extract the information from the span
                    # ignoring the other information in line
                    for span in line["spans"]:
                        # only get the size
                        df['file'].append(filename)
                        df["page"].append(page)
                        df["block"].append(block_num)
                        df["xmin"].append(span["bbox"][0])
                        df["ymin"].append(span["bbox"][1])
                        df["xmax"].append(span["bbox"][2])
                        df["ymax"].append(span["bbox"][3])
                        df["text"].append(span["text"])
                        df["font_size"].append(round(span["size"], precision_dp))
                        df["font_characteristics"].append(span["flags"])
                        df["font"].append(span["font"])
                        df["font_color"].append(span["color"])
                        df["image"].append("")
            block_num += 1

    # convert to dataframe
    df = pd.DataFrame(df) 

    # Remove trailing spaces
    df["text"] = df["text"].apply(lambda x: x.strip())

    # remove text fields that is empty
    df.drop(df[df["text"] == ""].index, inplace=True)

    df["text_rep"] = df["text"].apply(lambda x: df["text"].value_counts()[x])
    # we round to 4 decimal places so as to account for certain slight shifts in standardised content across multiple pages in the same pdf.
    # This could be due to content like header and footer
    df["xmin_rep"] = (
        df["xmin"]
        .round(precision_dp)
        .apply(lambda x: df["xmin"].round(precision_dp).value_counts()[x])
    )
    df["ymin_rep"] = (
        df["ymin"]
        .round(precision_dp)
        .apply(lambda x: df["ymin"].round(precision_dp).value_counts()[x])
    )
    df["cat"] = None

    MOST_FREQ_FONT_SIZE = df["font_size"].value_counts().index[0]
    MOST_FREQ_FONT = df["font"].value_counts().index[0]

    TOC_PAGES = toc_pages
    # get the last page number minus the number of pages that we define as table of content
    CONTENT_PAGES = page - TOC_PAGES

    # create a rounded xmin_round ymin_round col to account for subscript, superscript position in the same line
    df["xmin_round"] = df["xmin"].apply(lambda x: round(x, 1))
    df["ymin_round"] = df["ymin"].apply(lambda x: round(x, 0))

    # sort the values so that it appears in a top to down, left to right format
    df = df.sort_values(
        ["page", "ymin_round", "xmin_round"], ascending=[True, True, True]
    )

    # reset index
    df.reset_index(drop=True, inplace=True)

    # check if the block is part of a numbering list
    # eg. 1) text...
    prev_ymin = None
    prev_block = None
    for idx, row in df.iterrows():
        # ignore the first row
        # detect if it is a new row
        # if its a new row detect if text starts with common numbering list patterns
        # 1., 2.3.1, 1), a., a), A., A) using
        # length of text should be less than 10 (to give leeway for multi-level numbering list)
        # start with numbers, alphabet
        # ends with ")", ".", numbers or alphabets
        if (
            idx > 0
            and abs(row["ymin"] - prev_ymin) > 5
            and len(row["text"]) < 10
            and re.search("^[0-9a-zA-Z]{1}[0-9.]*[0-9).]{1}$", row["text"])
        ):
            df.loc[idx, "list_block"] = True
            prev_list = True
        # if prev row is a list and current row belong to the same block as previous row
        # then classify it as a list block as well
        elif row["block"] == prev_block and prev_list == True:
            df.loc[idx, "list_block"] = True
            prev_list = True
        else:
            df.loc[idx, "list_block"] = False
            prev_list = False
        prev_ymin = row["ymin"]
        prev_block = row["block"]

    return (
        df,
        file_dict["width"],
        file_dict["height"],
        page,
        MOST_FREQ_FONT_SIZE,
        MOST_FREQ_FONT,
        TOC_PAGES,
        CONTENT_PAGES,
    )


# extract line information from pdf
def pdf2line(path):
    doc = fitz.open(path)

    df_line = {
        "page": [],
        "xmin": [],
        "ymin": [],
        "xmax": [],
        "ymax": [],
        "width": [],
        "height": [],
    }

    for page_no, page in enumerate(doc):
        for p in page.get_drawings():
            # get rid of the weird point object
            # also ignore lines where fill is (1.0,1.0,1.0)
            # this seems abit weird as pymupdf detects all lines/rectangles. sometimes,
            # each line in a normal paragraph might be construed as a rectangle as well
            # however, the fill color seems to be wrong. (1.0, 1.0, 1.0) is black (RGB)
            # but what we see on the pdf is transparent
            if p["items"][0][0] != "re" or p["fill"] == (1.0, 1.0, 1.0):
                continue
            if p["items"][0][1].width > 10 or p["items"][0][1].height > 10:
                df_line["page"].append(page_no + 1)
                df_line["xmin"].append(p["items"][0][1][0])
                df_line["ymin"].append(p["items"][0][1][1])
                df_line["xmax"].append(p["items"][0][1][2])
                df_line["ymax"].append(p["items"][0][1][3])
                df_line["width"].append(p["items"][0][1].width)
                df_line["height"].append(p["items"][0][1].height)

    df_line = pd.DataFrame(df_line)

    # sort the values so that it appears in a top to down, left to right format
    df_line = df_line.sort_values(
        ["page", "ymin", "xmin"], ascending=[True, True, True]
    )
    df_line["table"] = None

    # reset index
    df_line.reset_index(drop=True, inplace=True)

    return df_line


# check if row is table of content
def is_toc(page, cat, TOC_PAGES):
    if page <= TOC_PAGES:
        return "toc"
    return cat


# check if row is header or footer
def is_header_footer(
    text_rep, xmin_rep, ymin_rep, ymin, CONTENT_PAGES, PAGE_HEIGHT, cat
):
    if cat != None:
        return cat
    if (
        (text_rep >= CONTENT_PAGES)
        and (xmin_rep >= CONTENT_PAGES)
        and (ymin_rep >= CONTENT_PAGES)
    ):
        if ymin < PAGE_HEIGHT * 0.25:
            return "header"
        elif ymin > PAGE_HEIGHT * 0.75:
            return "footer"
    return cat


# check if row is page number
def is_page_number(text, page, ymin_rep, TOC_PAGES, CONTENT_PAGES, cat):
    if cat != None:
        return cat
    # if the text equals to page number
    # or if "Page" and "of" are both found in text
    # treat the text as "page_number"
    if (text == str(page - TOC_PAGES) and ymin_rep >= CONTENT_PAGES) or (
        "Page" in text and "of" in text and ymin_rep >= CONTENT_PAGES
    ):
        # if ymin < PAGE_HEIGHT*0.25 or ymin > PAGE_HEIGHT*0.75:
        return "page_number"
    return cat


# check for table coordinates
def pdf_get_table_cood(path, toc_pages=2, gap_thres=10):
    df_line = pdf2line(path)

    if df_line.empty:
        return

    # Detect and label the tables
    # there could be multiple tables per page
    last_ymin = 0
    last_ymax = 0
    last_table = None
    recurrence = 0
    table_no = 1
    for idx, row in df_line[df_line["page"] > toc_pages].iterrows():
        # we have to add abs(row.ymin-last_ymax)<gap_thres becasue the table line detected are not
        # always correct. there could be duplicated lines detected although visually
        # it seems like it's only 1 line
        # Presume that more than gap_thres means a break in the table
        if (
            abs(row.ymin - last_ymin) < gap_thres
            or abs(row.ymin - last_ymax) < gap_thres
            or abs(row.ymax - last_ymax) < gap_thres
        ):
            recurrence += 1
            # print(idx, table_no)
        elif last_table != None:
            table_no += 1
            recurrence = 0

        if recurrence >= 2:
            # we have to access the df directly as iterrows provide a COPY of the dataframe
            # and are not actual access
            df_line.loc[idx, "table"] = table_no
            last_table = table_no
        else:
            last_table = None
            # print(df_line.loc[idx, 'table'])
            # print(idx,recurrence, table_no, row)

        last_ymin = row.ymin
        last_ymax = row.ymax

    df_table = {
        "page": [],
        "table": [],
        "xmin": [],
        "ymin": [],
        "xmax": [],
        "ymax": [],
    }

    for i in range(1, df_line["table"].max() + 1):
        df_table["page"].append(
            int(df_line[df_line["table"] == i].describe().loc["min", "page"])
        )
        df_table["table"].append(i)
        df_table["xmin"].append(
            df_line[df_line["table"] == i].describe().loc["min", "xmin"]
        )
        df_table["ymin"].append(
            df_line[df_line["table"] == i].describe().loc["min", "ymin"]
        )
        df_table["xmax"].append(
            df_line[df_line["table"] == i].describe().loc["max", "xmax"]
        )
        df_table["ymax"].append(
            df_line[df_line["table"] == i].describe().loc["max", "ymax"]
        )

    df_table = pd.DataFrame(df_table)
    return df_table


# check for tables based on df_table
def is_table(df, df_table):
    for idx, row in df_table.iterrows():
        row_indexes = df[
            (df["page"] == row.page)
            & (df["ymin"] > math.floor(row.ymin))
            & (df["ymax"] < math.ceil(row.ymax))
        ].index
        # iter through the each row in the df
        # if the category is currently None,
        # then change it to "table"
        for idx in row_indexes:
            if df.loc[idx, "cat"] is None:
                df.loc[idx, "cat"] = "table"
    return df


# check for footnote
def is_footnote(df, MOST_FREQ_FONT_SIZE):
    # sort it so that the bottom of each page would be at the top
    df = df.sort_values(
        ["page", "ymin_round", "xmin_round"], ascending=[True, False, True]
    )
    df.reset_index(drop=True, inplace=True)

    # then loop through each row of each page downwards (or basically, looking from bottom of page upwards)
    # good usage of iterrows instead of apply as we need to reference the previous row's cat in realtime instead of just applying fixed values based on current row values
    for page in df.page.unique():
        for page_idx, (index, row) in enumerate(df[df["page"] == page].iterrows()):
            # if it is the first row of each page and
            # also if the font size is smaller than most frequent font size
            # and also if it does not already have a set category
            # then treat it as footnote
            if (
                page_idx == 0
                and (row["font_size"] < MOST_FREQ_FONT_SIZE)
                and row["cat"] == None
            ):
                df.loc[index, "cat"] = "footnote"

            # Otherwise, if only the index is 0 or if there's already cat specified, then continue to next iteration
            if (page_idx == 0) or (row["cat"] != None):
                continue
            # if the previous row category is footer, page number or footnote,
            # and the font size is smaller than most freq font size
            # then deem this current row as footnote
            if (df.loc[index - 1, "cat"] in ["footer", "page_number", "footnote"]) and (
                row["font_size"] < MOST_FREQ_FONT_SIZE
            ):
                df.loc[index, "cat"] = "footnote"

    # change the sorting back to normal top down, left right
    df = df.sort_values(
        ["page", "ymin_round", "xmin_round"], ascending=[True, True, True]
    )
    df.reset_index(drop=True, inplace=True)

    return df


# check for main context text
def is_content(font_size, font, cat, MOST_FREQ_FONT_SIZE, MOST_FREQ_FONT):
    if cat != None:
        return cat
    if font_size == MOST_FREQ_FONT_SIZE and font == MOST_FREQ_FONT:
        return "content"
    return cat


# rank the remaining font characteristics based on font_size and font_style
def get_heading_dict(df, MOST_FREQ_FONT_SIZE):
    # pandas str.contains accept regex
    # we add a \ before + so as to escape it as a special char in regex
    pattern = "|".join(["BoldItalic", "\+F6", "Italic", "\+F7", "Bold", "\+F1", "\+F2"])

    # we filter out those df rows where for the same block and page, there are 
    # no category defined
    # as well as those font with bold, italic or bolditalic characteristics
    # as we would classify this as headings
    df_headings = (
        # df[(df.groupby(["page", "block"])["cat"].transform(lambda x: all(value is None for value in x))) & (df["font"].str.contains(pattern))]
        df[(df["cat"].isna()) & (df["font"].str.contains(pattern))]
        .groupby(["font_size", "font"], as_index=False)
        .size()
        .sort_values("font_size", ascending=False)
        .reset_index(drop=True)
    )

    # create heading dictionary such that the remaining biggest font_size would be rank 1
    # while the subsequently font_size (until it matches the MOST_FREQ_FONT_SIZE) will
    # be in corresponding decreasing rank (2 and lower)
    heading_level = 1
    heading_dict = {}
    for font_size in df_headings["font_size"].unique():
        if font_size >= MOST_FREQ_FONT_SIZE:
            heading_dict[font_size] = heading_level
            heading_level += 1
        else:
            heading_dict[font_size] = "unsure"

    return heading_dict


# check for headings and categorise the rest as unsure
def is_heading_or_unsure(
    heading_dict, font_size, font, cat, list_block, is_block_all_none, MOST_FREQ_FONT_SIZE,
):
    if cat != None:
        return cat
    if "BoldItalic" in font or "+F6" in font:
        style = "superemphasis"
    elif "Italic" in font or "+F7" in font:
        style = "emphasis"
    elif "Bold" in font or "+F1" in font or "+F2" in font:
        style = "heading"
    else:
        style = "content"

    # CONDITION 1
    # for text whose font size bigger than most freq font_size,
    # CONDITION 2
    # we add 1 to the numbering if it is part of a list_block because it is quite common
    # that we have two paragraphs with the same font style and font size but one is in a
    # numbering list while the other is not. The one in the numbering list should be
    # a sub heading of the other heading (without numbering list)
    # adding True (list_block boolean) value automatically adds 1
    # CONDITION 3
    # A row can only be considered as heading only if there's no other category in the 
    # same block. For eg. the whole block must be NONE before it can be categorised as 
    # heading

    # return as heading, emphasis or super emphasis based on whether is it bold,
    # italic or both as well as the hierachy (bigger font and not part of a numbering
    # list will get a higher hierachy. 1 is highest)
    if font_size >= MOST_FREQ_FONT_SIZE and style != "content" and is_block_all_none:
        return style + " " + str(heading_dict[font_size] + list_block)
    # if there's any non None category in the same block, we treat it as "content"
    # could be a paragraph but with a bigger font and bold to emphasis some text only (not heading)
    elif font_size >= MOST_FREQ_FONT_SIZE and style != "content" and not is_block_all_none:
        return "content"
    elif style == "content":
        # If it is  bigger than most freq font size, but is normal font,
        # just treat it as normal content
        return style
    else:
        # if it is smaller than freq font size, treat as unsure
        return str(heading_dict[font_size])


# function to extract everything and categorise them accordingly
def pdf_extractor(path, toc_pages=2, gap_thres=10, precision_dp=2):
    (
        df,
        PAGE_WIDTH,
        PAGE_HEIGHT,
        NO_OF_PAGES,
        MOST_FREQ_FONT_SIZE,
        MOST_FREQ_FONT,
        TOC_PAGES,
        CONTENT_PAGES,
    ) = pdf2df(path, toc_pages = toc_pages, precision_dp= precision_dp)

    df_line = pdf2line(path)

    # table of content
    df["cat"] = df.apply(lambda x: is_toc(x.page, x["cat"], TOC_PAGES), axis=1)
    # header or footer
    df["cat"] = df.apply(
        lambda x: is_header_footer(
            x.text_rep,
            x.xmin_rep,
            x.ymin_rep,
            x.ymin,
            CONTENT_PAGES,
            PAGE_HEIGHT,
            x["cat"],
        ),
        axis=1,
    )
    # page number
    df["cat"] = df.apply(
        lambda x: is_page_number(
            x.text, x.page, x.ymin_rep, TOC_PAGES, CONTENT_PAGES, x["cat"]
        ),
        axis=1,
    )
    # table ymin and ymax
    df_table = pdf_get_table_cood(path, TOC_PAGES, gap_thres)
    # tables
    if df_table is not None:
        df = is_table(df, df_table)
    # footnote
    df = is_footnote(df, MOST_FREQ_FONT_SIZE)
    # content
    df["cat"] = df.apply(
        lambda x: is_content(
            x.font_size, x.font, x["cat"], MOST_FREQ_FONT_SIZE, MOST_FREQ_FONT
        ),
        axis=1,
    )
    # get heading_dict
    heading_dict = get_heading_dict(df, MOST_FREQ_FONT_SIZE)
    # header or unsure
    df["cat"] = df.apply(
        lambda x: is_heading_or_unsure(
            heading_dict,
            x.font_size,
            x.font,
            x["cat"],
            x.list_block,
            df[(df["page"]==x.page) &(df['block'] == x.block)&(~df['cat'].isnull())].empty,
            MOST_FREQ_FONT_SIZE,
        ),
        axis=1,
    )

    return df
