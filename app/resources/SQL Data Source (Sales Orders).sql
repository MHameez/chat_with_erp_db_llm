DELETE FROM [TS.DSO].[dbo].[Order_Statistics_Demo]
INSERT INTO [TS.DSO].[dbo].[Order_Statistics_Demo]
           ([Source Company]
           ,[Sales Order Number]
           ,[Customer Code]
           ,[Customer Name]
           ,[Customer Country Name]
           ,[Customer City]
           ,[Customer Classificaition]
           ,[Customer Registered Date]
           ,[Sales Person Name]
           ,[Cost Calculation Profile]
           ,[Order Date]
           ,[Delivery Date]
           ,[Delivery Type]
           ,[Total Cost Price]
           ,[Total Sales Price]
           ,[Packaging Cost Price]
           ,[Packaging Sales Price]
           ,[Transport Cost Price]
           ,[Transport Sales Price]
           ,[Certificate Cost Price]
           ,[Certificate Sales Price]
           ,[Plate Laser Cutting Time (Seconds)]
           ,[Plate Laser Cutting Cost Price]
           ,[Plate Laser Cutting Sales Price]
           ,[Plate Laser Cutting Time Surcharge]
           ,[Plate Silking Time (Seconds)]
           ,[Plate Silking Cost Price]
           ,[Plate Silking Sales Price]
           ,[Plate Silking Time Surcharge]
           ,[Plate Bending Time (Seconds)]
           ,[Plate Bending Cost Price]
           ,[Plate Bending Sales Price]
           ,[Plate Bending Time Surcharge]
           ,[Plate Material Cost Price]
           ,[Plate Material Sales Price]
           ,[Plate Material Weight (kg)]
           ,[Plate Material Weight Surcharge]
           ,[Tube Laser Cutting Time (Seconds)]
           ,[Tube Laser Cutting Cost Price]
           ,[Tube Laser Cutting Sales Price]
           ,[Tube Laser Cutting Time Surcharge]
           ,[Tube Material Cost Price]
           ,[Tube Material Sales Price]
           ,[Tube Material Length (m)]
           ,[Tube Material Length Surcharge]
           ,[Material Residue Surcharge]
           ,[Customer Credit Surcharge]
           ,[Order Amount Surcharge]
           ,[Production Site Location]
           ,[Order Cancelled Status])

SELECT 
    [source_company] AS [Source Company],
    [SalesOrder] AS [Sales Order Number],
    [CustomerCode] AS [Customer Code],
    C.customer_name AS [Customer Name],
    C.customer_country_name AS [Customer Country Name],
	c.customer_city as [Customer City],
	c.abc_code [Customer Classificaition],
	c.customer_created_date as [Customer Registered Date] ,
	c.[salesperson_name] AS [Sales Person Name],
	c.[customer_calculation_profile] [Cost Calculation Profile],
    CAST([OrderDate] AS DATE) AS [Order Date],
    CAST([DeliveryDate] AS DATE) AS [Delivery Date],
    CASE 
        WHEN [DeliveryCategoryIndex] = 0 THEN 'Sprinter' 
        ELSE 'Normal' 
    END AS [Delivery Type],
    [CostPrice] AS [Total Cost Price],
    [SalesPrice] AS [Total Sales Price],
    [PackagingCostPrice] AS [Packaging Cost Price],
    [PackagingSalesPrice] AS [Packaging Sales Price],
    [TransportCostPrice] AS [Transport Cost Price],
    [TransportSalesPrice] AS [Transport Sales Price],
    [CertificateCostPrice] AS [Certificate Cost Price],
    [CertificateSalesPrice] AS [Certificate Sales Price],
    [PlcOperationTime] AS [Plate Laser Cutting Time (Seconds)],
    [PlcOperationCostPrice] AS [Plate Laser Cutting Cost Price],
    [PlcOperationSalesPrice] AS [Plate Laser Cutting Sales Price],
    [PlcOperationTimeSurcharge] AS [Plate Laser Cutting Time Surcharge],
    [PsOperationTime] AS [Plate Silking Time (Seconds)],
    [PsOperationCostPrice] AS [Plate Silking Cost Price],
    [PsOperationSalesPrice] AS [Plate Silking Sales Price],
    [PsOperationTimeSurcharge] AS [Plate Silking Time Surcharge],
    [PbOperationTime] AS [Plate Bending Time (Seconds)],
    [PbOperationCostPrice] AS [Plate Bending Cost Price],
    [PbOperationSalesPrice] AS [Plate Bending Sales Price],
    [PbOperationTimeSurcharge] AS [Plate Bending Time Surcharge],
    [PlateMaterialCostPrice] AS [Plate Material Cost Price],
    [PlateMaterialSalesPrice] AS [Plate Material Sales Price],
    [PlateMaterialWeight] AS [Plate Material Weight (kg)],
    [PlateMaterialWeightSurcharge] AS [Plate Material Weight Surcharge],
    [TlcOperationTime] AS [Tube Laser Cutting Time (Seconds)],
    [TlcOperationCostPrice] AS [Tube Laser Cutting Cost Price],
    [TlcOperationSalesPrice] AS [Tube Laser Cutting Sales Price],
    [TlcOperationTimeSurcharge] AS [Tube Laser Cutting Time Surcharge],
    [TubeMaterialCostPrice] AS [Tube Material Cost Price],
    [TubeMaterialSalesPrice] AS [Tube Material Sales Price],
    [TubeMaterialLength] AS [Tube Material Length (m)],
    [TubeMaterialLengthSurcharge] AS [Tube Material Length Surcharge],
    [MaterialResidueSurcharge] AS [Material Residue Surcharge],
    [CustomerCreditSurcharge] AS [Customer Credit Surcharge],
    [OrderAmountSurcharge] AS [Order Amount Surcharge],
    [LocationCode] AS [Production Site Location],
    [IsCancelled] AS [Order Cancelled Status]
FROM 
    [TS.DWHSTG].[nav].[Sales_Order_Statistic_2] s
JOIN 
    [TS.DWH].[dbo].[dim_customers] c 
    ON c.customer_id = s.CustomerCode 
    AND c.level_type = 'Customer' 
    AND c.intercompany_flag = 'N' 
    AND c.current_flag = 'Y'
WHERE 
    YEAR(S.OrderDate) >= 2023 
    AND S.delta_tombstone = 0
ORDER BY 
    [Order Date] DESC;
