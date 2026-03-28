import pandas as pd
import logging
from sqlalchemy import create_engine
import numpy as np
from ingestion_db import ingest_db
from ingestion_db import get_engine

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename ="logs/get_vendor_summary.log",
    level =logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
    force = True
)

def create_vendor_summary(engine):
    ''' this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query(""" 
    WITH FreightSummary AS (
        SELECT 
            VendorNumber, 
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    
    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY 
            p.VendorNumber, 
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),
    
    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )
    
    SELECT 
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """, engine)
    return vendor_sales_summary

def clean_data(df):
    """
    Cleans and prepares vendor sales data for analysis and database storage
    """

    # Convert datatype
    df['Volume'] = df['Volume'].astype(float)

    # Fill missing values
    df.fillna(0, inplace=True)

    # Remove spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    # Create KPIs

    # Gross Profit
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    # Profit Margin (safe division)
    df['ProfitMargin'] = np.where(
        df['TotalSalesDollars'] == 0,0,
        (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    )


    df['StockTurnover'] = np.where(
        df['TotalPurchaseQuantity'] == 0,0,df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    )

    # Sales to Purchase Ratio
    df['SalesToPurchaseRatio'] = np.where(
        df['TotalPurchaseDollars'] == 0,0,df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    )

    # Replace infinite values
    df.replace([np.inf, -np.inf], 0, inplace=True)

    return df

if __name__ == '__main__':
   #DB Connection
    engine = get_engine()

    logging.info("Creating a Vendor Summary Table......")
    summary_df = create_vendor_summary(engine)
    logging.info(summary_df.head())

    logging.info("Cleaning Data.........")
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())


    logging.info("Ingesting data.............")
    ingest_db(clean_df,'vendor_sales_summary',engine)
    logging.info("Completed")
    