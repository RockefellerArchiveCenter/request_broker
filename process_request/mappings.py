# 'AeonField': 'field_or_callable',
AEON = {
    "EADNumber": 'ead_id',
    "CallNumber": "resource_id",
    "GroupingField": "get_grouping_field",
    "ItemAuthor": "get_resource_creators",
    "ItemCitation": "uri",
    "ItemDate": "get_dates",
    "ItemInfo1": "title",
    "ItemInfo2": "get_rights_text",
    "ItemInfo3": "uri",
    "ItemInfo4": "description",
    "ItemInfo5": "get_restricted_in_container",
    "ItemNumber": "get_barcode",
    "ItemSubtitle": "get_parent_title",
    "ItemTitle": "get_collection_title",
    "ItemVolume": "get_container",
    "ItemIssue": "get_subcontainer",
    "Location": "get_location"
}

CSV = {
    "Title": "title",
    "URL": "get_dimes_url",
    "Creator(s)": "get_creators",
    "Dates": "get_dates",
    "Size": "get_size",
    "Collection Name": "get_collection_title",
    "Parent Collection Name": "get_parent_title",
}

EMAIL = {
    "Title": "title",
    "URL": "get_dimes_url",
    "Creator(s)": "get_creators",
    "Dates": "get_dates",
    "Size": "get_size",
    "Collection Name": "get_collection_title",
    "Parent Collection Name": "get_parent_title",
}
