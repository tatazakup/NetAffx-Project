import sqlite3

conn = sqlite3.connect('NetAffx.db') 
c = conn.cursor()

# SNP Annotation {MainData}
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS SNP_AN
    (
        RS_ID          CHAR(25)     NOT NULL    PRIMARY KEY,
        PROBE_ID        CHAR(25)     NOT NULL,
        CHROMOSOME     INT          NOT NULL,
        SOURCE         CHAR(20)     NOT NULL
    );
    '''
)

# SNP annotation file has AssociatedGene {MainData}
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS SNP_AN_AS
    (
        RS_ID          CHAR(25)     NOT NULL    PRIMARY KEY,
        GENE_ID        INT          NOT NULL,
        GENE_SYMBOL    CHAR(20)     NOT NULL,
        FOREIGN KEY(RS_ID) REFERENCES SNP_AN(RS_ID)
    );
    '''
)

# Annotation AssociatedGene details
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS AN_AS_DETAIL
    (
        DETAIL_ID       INT         NOT NULL    PRIMARY KEY,
        RS_ID          CHAR(25)     NOT NULL,
        DISTANCE       INT          NOT NULL,
        RELATIONSHIP   CHAR(10)     NOT NULL,
        FOREIGN KEY(RS_ID) REFERENCES SNP_AN_AS(RS_ID)
    );
    '''
)

# AlsoKnownAs (Ncbi website)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS ALSO_KNOW_AS
    (
        GENE_ID        INT          NOT NULL    PRIMARY KEY,
        OTHER_SYMBOL   INT          NULL,
        UPDATE_AT      DATETIME     NOT NULL,
        FOREIGN KEY(GENE_ID) REFERENCES SNP_AN_AS(GENE_ID)
    );
    '''
)

# Disease (7 name disease on focus)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS DISEASE
    (
        DISEASE_ID     INT          NOT NULL    AUTOINCREMENT   PRIMARY KEY,
        DISEASE_NAME   CHAR(200)    NOT NULL
    );
    '''
)

# Disease has AssociatedGene (Disease website)
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS DISEASE_AS
    (
        GENE_SYMBOL    CHAR(20)     NOT NULL    PRIMARY KEY,
        DISEASE_ID     INT          NOT NULL,
        FOREIGN KEY(DISEASE_ID) REFERENCES DISEASE(DISEASE_ID)
    );
    '''
)

# AssociatedGene From Source 
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS AS_SOURCE
    (
        GENE_SYMBOL    CHAR(20)     NOT NULL    PRIMARY KEY,
        SOURCE         INT          NOT NULL,
        FOREIGN KEY(GENE_SYMBOL) REFERENCES DISEASE_AS(GENE_SYMBOL)
    );
    '''
)

# SNP anotation rerated to Disease
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS SNP_AN_DISEASE
    (
        RS_ID            CHAR(25)    NOT NULL,
        DISEASE_ID       INT         NOT NULL,
        FOREIGN KEY(RS_ID) REFERENCES SNP_AN(RS_ID),
        FOREIGN KEY(DISEASE_ID) REFERENCES DISEASE(DISEASE_ID)
    );
    '''
)

conn.commit()
conn.close()