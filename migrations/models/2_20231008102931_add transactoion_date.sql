-- upgrade --
ALTER TABLE "expenses" ADD "transaction_date" TIMESTAMPTZ NULL;
-- downgrade --
ALTER TABLE "expenses" DROP COLUMN "transaction_date";
