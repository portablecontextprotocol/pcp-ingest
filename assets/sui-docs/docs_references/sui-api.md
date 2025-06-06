Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Sui RPC
    * GraphQL (Alpha)
    * JSON-RPC
    * Sui Full Node gRPC
    * RPC Best Practices
  * Sui CLI
    * Sui CLI Cheat Sheet
    * Sui Client CLI
    * Sui Client PTB CLI
    * Sui Console CLI
    * Sui Keytool CLI
    * Sui Move CLI
    * Sui Validator CLI
  * Sui IDE Support
    * Move Analyzer
    * Move Trace Debugger
  * Sui SDKs
    * dApp Kit
    * Rust SDK
    * TypeScript SDK
    * zkSend SDK
  * Move
    * Framework
    * The Move Book
    * The Move Reference
  * Glossary
  * Contribute


  *   * Sui RPC


On this page
# Sui RPC
Refer to Access Sui Data for an overview of options to access Sui network data.
_SuiJSON_ is a JSON-based format with restrictions that allow Sui to align JSON inputs more closely with Move call arguments.
This table shows the restrictions placed on JSON types to make them SuiJSON compatible:
JSON | SuiJSON Restrictions | Move Type Mapping  
---|---|---  
Number | Must be unsigned integer | u8, u6, u32, u64 (encoded as String), u128 (encoded as String), u256 (encoded as String)  
String | No restrictions | Vector`<u8>`, Address, ObjectID, TypeTag, Identifier, Unsigned integer (256 bit max)  
Boolean | No restrictions | Bool  
Array | Must be homogeneous JSON and of SuiJSON type | Vector  
Null | Not allowed | N/A  
Object | Not allowed | N/A  
## Type coercion reasoning​
Due to the loosely typed nature of JSON/SuiJSON and the strongly typed nature of Move types, you sometimes need to overload SuiJSON types to represent multiple Move types.
For example `SuiJSON::Number` can represent both _u8_ and _u32_. This means you have to coerce and sometimes convert types.
Which type you coerce depends on the expected Move type. For example, if the Move function expects a u8, you must have received a `SuiJSON::Number` with a value less than 256. More importantly, you have no way to easily express Move addresses in JSON, so you encode them as hex strings prefixed by `0x`.
Additionally, Move supports u128 and u256 but JSON doesn't. As a result Sui allows encoding numbers as strings.
## Type coercion rules​
Move Type | SuiJSON Representations | Valid Examples | Invalid Examples  
---|---|---|---  
Bool | Bool | true, false |   
u8 | Supports 3 formats: Unsigned number < 256. Decimal string with value < 256. One byte hex string prefixed with 0x. | 7 "70" "0x43" | -5: negative not allowed 3.9: float not allowed NaN: not allowed 300: U8 must be less than 256 " 9": Spaces not allowed in string "9A": Hex num must be prefixed with 0x "0x09CD": Too large for U8  
u16 | Three formats are supported Unsigned number < 65536. Decimal string with value < 65536. Two byte hex string prefixed with 0x. | 712 "570" "0x423" | -5: negative not allowed 3.9: float not allowed NaN: not allowed 98342300: U16 must be less than 65536 " 19": Spaces not allowed in string "9EA": Hex num must be prefixed with 0x "0x049C1D": Too large for U16  
u32 | Three formats are supported Unsigned number < 4294967296. Decimal string with value < 4294967296. One byte hex string prefixed with 0x. | 9823247 "987120" "0x4BADE93" | -5: negative not allowed 3.9: float not allowed NaN: not allowed 123456789123456: U32 must be less than 4294967296 " 9": Spaces not allowed in string "9A": Hex num must be prefixed with 0x "0x3FF1FF9FFDEFF": Too large for U32  
u64 | Supports two formats Decimal string with value < U64::MAX. Up to 8 byte hex string prefixed with 0x. | "747944370" "0x2B1A39A15E" | 123434: Although this is a valid U64 number, it must be encoded as a string  
u128 | Two formats are supported Decimal string with value < U128::MAX. Up to 16 byte hex string prefixed with 0x. | "74794734937420002470" "0x2B1A39A1514E1D8A7CE" | 34: Although this is a valid U128 number, it must be encoded as a string  
u256 | Two formats are supported Decimal string with value < U256::MAX. Up to 32 byte hex string prefixed with 0x. | "747947349374200024707479473493742000247" "0x2B1762FECADA39753FCAB2A1514E1D8A7CE" | 123434: Although this is a valid U256 number, it must be encoded as a string 0xbc33e6e4818f9f2ef77d020b35c24be738213e64d9e58839ee7b4222029610de  
Address | 32 byte hex string prefixed with 0x | "0xbc33e6e4818f9f2ef77d020b35c24be738213e64d9e58839ee7b4222029610de" | 0xbc33: string too short bc33e6e4818f9f2ef77d020b35c24be738213e64d9e58839ee7b4222029610de: missing 0x prefix 0xG2B1A39A1514E1D8A7CE45919CFEB4FEE70B4E01: invalid hex char G  
ObjectID | 32 byte hex string prefixed with 0x | "0x1b879f00b03357c95a908b7fb568712f5be862c5cb0a5894f62d06e9098de6dc" | Similar to above  
Identifier | Typically used for module and function names. Encoded as one of the following: A String whose first character is a letter and the remaining characters are letters, digits or underscore. A String whose first character is an underscore, and there is at least one further letter, digit or underscore | "function", "_function", "some_name", "____some_name", "Another" | "_": missing trailing underscore, digit or letter, "8name": cannot start with digit, ".function": cannot start with period, " ": cannot be empty space, "func name": cannot have spaces  
Vector`<Move Type>` / Option`<Move Type>` | Homogeneous vector of aforementioned types including nested vectors of primitive types (only "flat" vectors of ObjectIDs are allowed) | [1,2,3,4]: simple U8 vector [[3,600],[],[0,7,4]]: nested U32 vector ["0x2B1A39A1514E1D8A7CE45919CFEB4FEE", "0x2B1A39A1514E1D8A7CE45919CFEB4FEF"]: ObjectID vector | [1,2,3,false]: not homogeneous JSON [1,2,null,4]: invalid elements [1,2,"7"]: although Sui allows encoding numbers as strings meaning this array can evaluate to [1,2,7], the array is still ambiguous so it fails the homogeneity check.  
Vector`<u8>` | For convenience, Sui allows: U8 vectors represented as UTF-8 (and ASCII) strings. | "√®ˆbo72 √∂†∆˚–œ∑π2ie": UTF-8 "abcdE738-2 _=?": ASCII |   
Previous
Overview
Next
GraphQL (Beta)
  * Type coercion reasoning
  * Type coercion rules


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
