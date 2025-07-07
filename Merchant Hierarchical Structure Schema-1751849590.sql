CREATE TABLE "Merchants" (
	"MerchantID"  NOT NULL,
	"MerchantName" varchar2(255) NOT NULL DEFAULT '255',
	"MerchantType" varchar2(255) NOT NULL DEFAULT '100',
	"ContactEmail" varchar2(255) NOT NULL DEFAULT '255',
	"ContactPhone" varchar2(255) DEFAULT '15',
	"AddressLine1" varchar2(255) DEFAULT '255',
	"AddressLine2" varchar2(255) DEFAULT '255',
	"City" varchar2(255) NOT NULL DEFAULT '100',
	"State" varchar2(255) NOT NULL DEFAULT '100',
	"ZipCode" varchar2(255) NOT NULL DEFAULT '10',
	"Country" varchar2(255) NOT NULL DEFAULT '100',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"ParentMerchantID" ,
	PRIMARY KEY ("MerchantID")
);

CREATE TABLE "MerchantCategories" (
	"CategoryID"  NOT NULL,
	"CategoryName" varchar2(255) NOT NULL DEFAULT '255',
	"Description" varchar2(255) DEFAULT '500',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"ParentCategoryID" ,
	PRIMARY KEY ("CategoryID")
);

CREATE TABLE "MerchantProducts" (
	"ProductID"  NOT NULL,
	"MerchantID"  NOT NULL,
	"ProductName" varchar2(255) NOT NULL DEFAULT '255',
	"Description" varchar2(255) DEFAULT '500',
	"Price"  NOT NULL,
	"StockQuantity"  NOT NULL,
	"SKU" varchar2(255) DEFAULT '100',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"CategoryID" ,
	PRIMARY KEY ("ProductID")
);

CREATE TABLE "MerchantReviews" (
	"Rating"  NOT NULL,
	"ReviewID"  NOT NULL,
	"CustomerID"  NOT NULL,
	"ReviewText" varchar2(255) DEFAULT '1000',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"HelpfulVotes" ,
	"ReportCount" ,
	"ResponseText" varchar2(255) DEFAULT '1000',
	"ResponseDate" date,
	"ResponseStatus" varchar2(255) DEFAULT '50',
	"CustomerName" varchar2(255) DEFAULT '255',
	"MerchantID"  NOT NULL,
	"CustomerEmail" varchar2(255) DEFAULT '255',
	PRIMARY KEY ("ReviewID")
);

CREATE TABLE "Customers" (
	"CustomerID"  NOT NULL,
	"FirstName" varchar2(255) NOT NULL DEFAULT '100',
	"LastName" varchar2(255) NOT NULL DEFAULT '100',
	"Email" varchar2(255) NOT NULL DEFAULT '255',
	"Phone" varchar2(255) DEFAULT '15',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"AddressLine1" varchar2(255) DEFAULT '255',
	"AddressLine2" varchar2(255) DEFAULT '255',
	"City" varchar2(255) DEFAULT '100',
	"State" varchar2(255) DEFAULT '100',
	"ZipCode" varchar2(255) DEFAULT '10',
	"Country" varchar2(255) DEFAULT '100',
	"DateOfBirth" date,
	"Gender" varchar2(255) DEFAULT '10',
	"LoyaltyPoints" ,
	PRIMARY KEY ("CustomerID")
);

CREATE TABLE "MerchantTransactions" (
	"TransactionID"  NOT NULL,
	"CustomerID"  NOT NULL,
	"TransactionDate" date NOT NULL,
	"Amount"  NOT NULL,
	"PaymentMethod" varchar2(255) NOT NULL DEFAULT '50',
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"TransactionType" varchar2(255) NOT NULL DEFAULT '50',
	"Currency" varchar2(255) NOT NULL DEFAULT '10',
	"DiscountApplied" ,
	"TaxAmount" ,
	"RefundAmount" ,
	"MerchantID"  NOT NULL,
	"Notes" varchar2(255) DEFAULT '500',
	PRIMARY KEY ("TransactionID")
);

CREATE TABLE "MerchantPromotions" (
	"PromotionID"  NOT NULL,
	"MerchantID"  NOT NULL,
	"PromotionName" varchar2(255) NOT NULL DEFAULT '255',
	"Description" varchar2(255) DEFAULT '500',
	"StartDate" date NOT NULL,
	"EndDate" date NOT NULL,
	"DiscountPercentage" ,
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"MaxUsageLimit" ,
	"MinPurchaseAmount" ,
	"ApplicableCategories" varchar2(255) DEFAULT '500',
	"PromotionCode" varchar2(255) DEFAULT '100',
	"UsageCount" ,
	PRIMARY KEY ("PromotionID")
);

CREATE TABLE "MerchantSettings" (
	"IsRequired" ,
	"SettingID"  NOT NULL,
	"MerchantID"  NOT NULL,
	"SettingKey" varchar2(255) NOT NULL DEFAULT '100',
	"SettingValue" varchar2(255) NOT NULL DEFAULT '255',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"Description" varchar2(255) DEFAULT '500',
	"IsActive" ,
	"LastUpdatedBy" varchar2(255) DEFAULT '100',
	"DataType" varchar2(255) DEFAULT '50',
	"ValidationRules" varchar2(255) DEFAULT '500',
	"DefaultValue" varchar2(255) DEFAULT '255',
	"Visibility" varchar2(255) DEFAULT '50',
	PRIMARY KEY ("SettingID")
);

CREATE TABLE "MerchantAnalytics" (
	"TotalVisitors"  NOT NULL,
	"AnalyticsID"  NOT NULL,
	"MerchantID"  NOT NULL,
	"Date" date NOT NULL,
	"TotalSales"  NOT NULL,
	"ConversionRate" ,
	"AverageOrderValue" ,
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"TotalRefunds" ,
	"TotalDiscounts" ,
	"CustomerFeedbackScore" ,
	"NewCustomers" ,
	"ReturningCustomers" ,
	"SalesGrowthRate" ,
	PRIMARY KEY ("AnalyticsID")
);

CREATE TABLE "MerchantNotifications" (
	"NotificationID"  NOT NULL,
	"MerchantID"  NOT NULL,
	"NotificationType" varchar2(255) NOT NULL DEFAULT '100',
	"Message" varchar2(255) NOT NULL DEFAULT '1000',
	"CreatedDate" date NOT NULL,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"IsRead" ,
	"Priority" varchar2(255) DEFAULT '50',
	"ExpirationDate" date,
	"SenderID" ,
	"RelatedTransactionID" ,
	"RelatedReviewID" ,
	"RelatedPromotionID" ,
	"RelatedCustomerID" ,
	"NotificationChannel" varchar2(255) DEFAULT '50',
	PRIMARY KEY ("NotificationID")
);

CREATE TABLE "MerchantTags" (
	"TagID"  NOT NULL,
	"MerchantID"  NOT NULL,
	"TagName" varchar2(255) NOT NULL DEFAULT '100',
	"CreatedDate" date NOT NULL,
	"UpdatedDate" date,
	"Status" varchar2(255) NOT NULL DEFAULT '50',
	"Description" varchar2(255) DEFAULT '500',
	"IsActive" ,
	"TagType" varchar2(255) DEFAULT '50',
	"RelatedCategoryID" ,
	"UsageCount" ,
	"CreatedBy" varchar2(255) DEFAULT '100',
	"UpdatedBy" varchar2(255) DEFAULT '100',
	"Visibility" varchar2(255) DEFAULT '50',
	"ColorCode" varchar2(255) DEFAULT '7',
	PRIMARY KEY ("TagID")
);

ALTER TABLE "Merchants" ADD CONSTRAINT "Merchants_fk14" FOREIGN KEY ("ParentMerchantID") REFERENCES "Merchants"("MerchantID");
ALTER TABLE "MerchantCategories" ADD CONSTRAINT "MerchantCategories_fk6" FOREIGN KEY ("ParentCategoryID") REFERENCES "MerchantCategories"("CategoryID");
ALTER TABLE "MerchantProducts" ADD CONSTRAINT "MerchantProducts_fk1" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");

ALTER TABLE "MerchantProducts" ADD CONSTRAINT "MerchantProducts_fk10" FOREIGN KEY ("CategoryID") REFERENCES "MerchantCategories"("CategoryID");
ALTER TABLE "MerchantReviews" ADD CONSTRAINT "MerchantReviews_fk2" FOREIGN KEY ("CustomerID") REFERENCES "Customers"("CustomerID");

ALTER TABLE "MerchantReviews" ADD CONSTRAINT "MerchantReviews_fk13" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");

ALTER TABLE "MerchantTransactions" ADD CONSTRAINT "MerchantTransactions_fk1" FOREIGN KEY ("CustomerID") REFERENCES "Customers"("CustomerID");

ALTER TABLE "MerchantTransactions" ADD CONSTRAINT "MerchantTransactions_fk13" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");
ALTER TABLE "MerchantPromotions" ADD CONSTRAINT "MerchantPromotions_fk1" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");
ALTER TABLE "MerchantSettings" ADD CONSTRAINT "MerchantSettings_fk2" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");
ALTER TABLE "MerchantAnalytics" ADD CONSTRAINT "MerchantAnalytics_fk2" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");
ALTER TABLE "MerchantNotifications" ADD CONSTRAINT "MerchantNotifications_fk1" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");
ALTER TABLE "MerchantTags" ADD CONSTRAINT "MerchantTags_fk1" FOREIGN KEY ("MerchantID") REFERENCES "Merchants"("MerchantID");