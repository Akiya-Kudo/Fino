INPUT = {
    "type": "object",
    "properties": {
        "detail": {
            "type": "object",
            "properties": {
                "document_ids": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
        },
        "detailType": {
            "type": "string",
        },
    },
    "required": ["detail", "detailType"],
    "additionalProperties": False,
}

OUTPUT = {
    "type": "object",
    "properties": {
        "status": {
            "type": "integer"
        },
        "detail": {
            "type": "object",
            "properties": {
                "document_ids": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
                "sec_code": {
                    "type": "string",
                },
            },
        },
        "detailType": {
            "type": "string",
        },
    },
    "required": ["detail", "detailType"],
    "additionalProperties": False,
}