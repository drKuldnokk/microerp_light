BEGIN;

DROP TABLE IF EXISTS "OrderLine";
DROP TABLE IF EXISTS "SalesOrder";
DROP TABLE IF EXISTS "Product";

CREATE TABLE "SalesOrder" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE "Product" (
    "id" varchar(20) NOT NULL PRIMARY KEY, 
    "name" varchar(500) NOT NULL
);

CREATE TABLE "OrderLine" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "quantity" integer NOT NULL, 
    "salesOrder" integer NOT NULL REFERENCES "SalesOrder" ("id"),
    "product" varchar(20) NOT NULL REFERENCES "Product" ("id")
);

CREATE INDEX "OrderLine_orderIdx" ON "OrderLine" ("salesOrder");
CREATE INDEX "OrderLine_productIdx" ON "OrderLine" ("product");

COMMIT;