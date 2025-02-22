import xml.etree.ElementTree as ET


def parse_yandex_search_xml(xml_data: str) -> dict:
    root = ET.fromstring(xml_data)

    request_elem = root.find("request")
    query = request_elem.find("query").text if request_elem is not None else None

    response_elem = root.find("response")
    found_elem = response_elem.find('found[@priority="phrase"]') if response_elem is not None else None
    found_phrase = found_elem.text if found_elem is not None else None

    results_list = []
    results_elem = response_elem.find("results") if response_elem is not None else None
    if results_elem is not None:
        grouping_elem = results_elem.find("grouping")
        if grouping_elem is not None:
            for group in grouping_elem.findall("group"):
                doc_elem = group.find("doc")
                if doc_elem is None:
                    continue

                doc_id = doc_elem.get("id")
                url_elem = doc_elem.find("url")
                url = url_elem.text if url_elem is not None else None

                image_props = doc_elem.find("image-properties")
                image_link = None
                thumbnail_link = None
                if image_props is not None:
                    img_link_elem = image_props.find("image-link")
                    thumb_link_elem = image_props.find("thumbnail-link")
                    image_link = img_link_elem.text if img_link_elem is not None else None
                    thumbnail_link = thumb_link_elem.text if thumb_link_elem is not None else None

                results_list.append({
                    "doc_id": doc_id,
                    "url": url,
                    "image_link": image_link,
                    "thumbnail_link": thumbnail_link,
                })

    return {
        "query": query,
        "found_phrase": found_phrase,
        "results": results_list
    }