# https://sejong.tracker.solidwallet.io/contract/cx162a79cc8eb19206cebeff47e2708cfc04f589b5

# IRC31_METHODS = [
#     {
#         "name": "ApprovalForAll",
#         "type": "eventlog",
#         "inputs": [
#             {
#                 "name": "_owner",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_operator",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_approved",
#                 "type": "bool"
#             }
#         ]
#     },
#     {
#         "name": "TransferBatch",
#         "type": "eventlog",
#         "inputs": [
#             {
#                 "name": "_operator",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_from",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_to",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_ids",
#                 "type": "bytes"
#             },
#             {
#                 "name": "_values",
#                 "type": "bytes"
#             }
#         ]
#     },
#     {
#         "name": "TransferSingle",
#         "type": "eventlog",
#         "inputs": [
#             {
#                 "name": "_operator",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_from",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_to",
#                 "type": "Address",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_id",
#                 "type": "int"
#             },
#             {
#                 "name": "_value",
#                 "type": "int"
#             }
#         ]
#     },
#     {
#         "name": "URI",
#         "type": "eventlog",
#         "inputs": [
#             {
#                 "name": "_id",
#                 "type": "int",
#                 "indexed": "0x1"
#             },
#             {
#                 "name": "_value",
#                 "type": "str"
#             }
#         ]
#     },
#     {
#         "name": "balanceOf",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_owner",
#                 "type": "Address"
#             },
#             {
#                 "name": "_id",
#                 "type": "int"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "int"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "balanceOfBatch",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_owners",
#                 "type": "[]Address"
#             },
#             {
#                 "name": "_ids",
#                 "type": "[]int"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "list"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "isApprovedForAll",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_owner",
#                 "type": "Address"
#             },
#             {
#                 "name": "_operator",
#                 "type": "Address"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "bool"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "name",
#         "type": "function",
#         "inputs": [],
#         "outputs": [
#             {
#                 "type": "str"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "setApprovalForAll",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_operator",
#                 "type": "Address"
#             },
#             {
#                 "name": "_approved",
#                 "type": "bool"
#             }
#         ],
#         "outputs": []
#     },
#     {
#         "name": "tokenURI",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_id",
#                 "type": "int"
#             }
#         ],
#         "outputs": [
#             {
#                 "type": "str"
#             }
#         ],
#         "readonly": "0x1"
#     },
#     {
#         "name": "transferFrom",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_from",
#                 "type": "Address"
#             },
#             {
#                 "name": "_to",
#                 "type": "Address"
#             },
#             {
#                 "name": "_id",
#                 "type": "int"
#             },
#             {
#                 "name": "_value",
#                 "type": "int"
#             },
#             {
#                 "name": "_data",
#                 "default": null,
#                 "type": "bytes"
#             }
#         ],
#         "outputs": []
#     },
#     {
#         "name": "transferFromBatch",
#         "type": "function",
#         "inputs": [
#             {
#                 "name": "_from",
#                 "type": "Address"
#             },
#             {
#                 "name": "_to",
#                 "type": "Address"
#             },
#             {
#                 "name": "_ids",
#                 "type": "[]int"
#             },
#             {
#                 "name": "_values",
#                 "type": "[]int"
#             },
#             {
#                 "name": "_data",
#                 "default": null,
#                 "type": "bytes"
#             }
#         ],
#         "outputs": []
#     }
# ]


IRC31_METHODS = [
    {
        "inputs": [{"name": "_owner", "type": "Address"}, {"name": "_id", "type": "int"}],
        "name": "balanceOf",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_owners", "type": "[]Address"}, {"name": "_ids", "type": "[]int"}],
        "name": "balanceOfBatch",
        "outputs": [{"type": "list"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "owner", "type": "Address"}],
        "name": "balanceOfAll",
        "outputs": [{"type": "list"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "_id", "type": "int"}],
        "name": "tokenURI",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [
            {"name": "_from", "type": "Address"},
            {"name": "_to", "type": "Address"},
            {"name": "_id", "type": "int"},
            {"name": "_value", "type": "int"},
            {"default": None, "name": "_data", "type": "bytes"},
        ],
        "name": "transferFrom",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "_from", "type": "Address"},
            {"name": "_to", "type": "Address"},
            {"name": "_ids", "type": "[]int"},
            {"name": "_values", "type": "[]int"},
            {"default": None, "name": "_data", "type": "bytes"},
        ],
        "name": "transferFromBatch",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_operator", "type": "Address"}, {"name": "_approved", "type": "bool"}],
        "name": "setApprovalForAll",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "_owner", "type": "Address"}, {"name": "_operator", "type": "Address"}],
        "name": "isApprovedForAll",
        "outputs": [{"type": "bool"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [
            {"indexed": "0x1", "name": "_operator", "type": "Address"},
            {"indexed": "0x1", "name": "_from", "type": "Address"},
            {"indexed": "0x1", "name": "_to", "type": "Address"},
            {"name": "_id", "type": "int"},
            {"name": "_value", "type": "int"},
        ],
        "name": "TransferSingle",
        "type": "eventlog",
    },
    {
        "inputs": [
            {"indexed": "0x1", "name": "_operator", "type": "Address"},
            {"indexed": "0x1", "name": "_from", "type": "Address"},
            {"indexed": "0x1", "name": "_to", "type": "Address"},
            {"name": "_ids", "type": "bytes"},
            {"name": "_values", "type": "bytes"},
        ],
        "name": "TransferBatch",
        "type": "eventlog",
    },
    {
        "inputs": [
            {"indexed": "0x1", "name": "_owner", "type": "Address"},
            {"indexed": "0x1", "name": "_operator", "type": "Address"},
            {"name": "_approved", "type": "bool"},
        ],
        "name": "ApprovalForAll",
        "type": "eventlog",
    },
    {
        "inputs": [
            {"indexed": "0x1", "name": "_id", "type": "int"},
            {"name": "_value", "type": "str"},
        ],
        "name": "URI",
        "type": "eventlog",
    },
    {
        "inputs": [{"name": "user", "type": "Address"}],
        "name": "addAdmin",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "user", "type": "Address"}],
        "name": "removeAdmin",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Lockdown",
        "outputs": [{"type": "bool"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "get_Num_Gens",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Egg_Price",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Egg_Supply",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_latest_Egg_ID",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "address", "type": "Address"}, {"name": "gen", "type": "int"}],
        "name": "get_Num_Eggs_Owned",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "lockdown_status", "type": "str"}, {"name": "gen", "type": "int"}],
        "name": "set_Lockdown",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "address", "type": "Address"},
            {"name": "index", "type": "int"},
            {"name": "gen", "type": "int"},
        ],
        "name": "get_EggID_Owner_Index",
        "outputs": [{"type": "int"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "tokenURIs", "type": "str"}, {"name": "gen", "type": "int"}],
        "name": "set_Possible_TokenURIs",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "empty_Possible_TokenURIs",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Possible_TokenURIs",
        "outputs": [{"type": "list"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Possible_TokenURIs_Count",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "global_egg_id", "type": "int"}],
        "name": "get_TokenURI",
        "outputs": [{"type": "str"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "price", "type": "int"}, {"name": "gen", "type": "int"}],
        "name": "set_Egg_Price",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "supply", "type": "int"}, {"name": "gen", "type": "int"}],
        "name": "set_Egg_Supply",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "num_gens", "type": "int"}],
        "name": "set_Num_Gens",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "address", "type": "Address"},
            {"name": "gen", "type": "int"},
            {"name": "seed", "type": "str"},
        ],
        "name": "owner_Mint",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [
            {"name": "address", "type": "Address"},
            {"name": "global_egg_id", "type": "int"},
            {"name": "gen_egg_id", "type": "int"},
            {"name": "gen", "type": "int"},
            {"name": "seed", "type": "str"},
        ],
        "name": "owner_Mint_TokenID",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Sale_Active",
        "outputs": [{"type": "bool"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}, {"name": "active", "type": "bool"}],
        "name": "set_Sale_Active",
        "outputs": [],
        "type": "function",
    },
    {
        "inputs": [{"name": "gen", "type": "int"}],
        "name": "get_Craft_Promotion",
        "outputs": [{"type": "bool"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "get_Treasury_Wallet",
        "outputs": [{"type": "Address"}],
        "readonly": "0x1",
        "type": "function",
    },
    {
        "inputs": [{"name": "address", "type": "Address"}],
        "name": "set_Treasury_Wallet",
        "outputs": [],
        "type": "function",
    },
]
