# !/usr/bin/env python3
# -*- coding = utf-8 -*-

request = {
    'first': {
'<SqlQuery><Conditions>\
<SC>\
<SLT>0</SLT>\
<PN>A.CLASS_ID</PN>\
<PV></PV>\
<SRT>0</SRT>\
<SPT>1</SPT>\
</SC><SC>\
<SLT>0</SLT>\
<PN>C.MAN_ID</PN>\
<PV></PV>\
<SRT>0</SRT>\
<SPT>1</SPT>\
</SC>\
</Conditions>\
<OrderString>\
ORDER BY A.CREATE_TIME DESC\
</OrderString>\
<IsPageResult>1</IsPageResult>\
<KeyId>A.OBJ_ID</KeyId>\
<PageInfo>\
<PageSize>20</PageSize>\
<CurrentPage>1</CurrentPage>\
<RowCount>0</RowCount>\
<PageCount>0</PageCount>\
<OrderBy>ORDER BY A.CREATE_TIME DESC</OrderBy>\
</PageInfo>\
<QueryTable>\
<TableName>BMP_OBJECT</TableName>\
        <AliasName>A</AliasName>\
        <JoinTables>\
            <JoinTable>\
                <JoinType>1</JoinType>\
                <QueryTable>\
                    <TableName>BMP_ATTRIBCLASS</TableName>\
                    <AliasName>B</AliasName>\
                </QueryTable>\
                <JoinCondition>A.CLASS_ID=B.CLASS_ID</JoinCondition>\
            </JoinTable>\
            <JoinTable>\
                <JoinType>1</JoinType>\
                <QueryTable>\
                    <TableName>BMP_MANUFACTURERS</TableName>\
                    <AliasName>C</AliasName>\
                </QueryTable>\
                <JoinCondition>A.NUM_VAL5=C.MAN_ID</JoinCondition>\
            </JoinTable>\
        </JoinTables>\
    </QueryTable>\
    <ResultFields>A.*,B.*,C.MAN_ID,C.MAN_NAME,C.FIELD_1 AS MODEL,(select group_concat(e.group_name) from BMP_OBJ2GROUP D left join bmp_objgroup E on D.GROUP_ID = E.GROUP_ID where D.OBJ_ID = a.obj_ID and e.group_type=1 ) as GROUP_NAME\
    </ResultFields>\
    </SqlQuery>'},

    'second': {
    '<SqlQuery>\
    <Conditions>\
        <SC>\
            <SLT>0</SLT>\
            <PN>A.CLASS_LEVEL</PN>\
            <PV>0</PV>\
            <SRT>0</SRT>\
            <SPT>0</SPT>\
        </SC>\
    </Conditions>\
    <KeyId>A.CLASS_ID</KeyId>\
    <QueryTable>\
        <TableName>bmp_attribclass</TableName>\
        <AliasName>A</AliasName>\
    </QueryTable>\
    <ResultFields>A.CLASS_ID,A.CLASS_NAME</ResultFields>\
    </SqlQuery>'},

    'third': {
    '<SqlQuery>\
    <Conditions></Conditions>\
    <KeyId>M.MAN_ID</KeyId>\
    <QueryTable>\
        <TableName>bmp_manufacturers</TableName>\
        <AliasName>M</AliasName>\
    </QueryTable>\
    <ResultFields>distinct M.MAN_NAME,M.MAN_NAME as MAN_ID</ResultFields>\
    </SqlQuery>'
    }
}

