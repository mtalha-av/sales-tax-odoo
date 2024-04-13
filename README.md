# Avior Tax Services Connector
This connector allows you to interact with the Avior Tax Services API which provides tax calculation services for all US states and territories. It is able use the company's address and the customer's address to calculate the tax for a given order.

## Pre-requisites

You will need an Avior Tax Services account, and Authentication credentials provided by Avior Tax Services. Once you activate and configure the connector, it automatically perform tax calculations in the background.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
    1. [Configure Avior Tax Connection](#configure-avior-tax-connection)
    2. [Configure Taxes](#configure-taxes)
    3. [Configure Fiscal Positions](#configure-fiscal-positions)
3. [How to use](#how-to-use)

## Installation

1. Download the Avior Tax Services Connector from the [Odoo Apps Store](https://apps.odoo.com/apps).
2. Add the connector to your Odoo instance. This can be done by uploading the compressed connector file the Odoo instance's addons directory.
3. Login to your Odoo instance as an _administrator_, and navigate to **Settings** and activate the **Developer Mode**.
4. Then navigate to **Apps** and click the **Update Apps List** button. This will update the list of available apps. You may need to refresh the page if you do not see the connector.
5. Search for the Avior Tax Services Connector in the Apps list and click the **Install** button. This will install the connector to your Odoo instance as well as add a default Tax and Fiscal Position already configured to use Avior Tax Connector. It will also add a **county** field to the **res.partner** model.

## configuration

### Configure Avior Tax Connection
1. Navigate to **Accounting** > **Configuration** > **Avior Tax** > **Avior Tax API**.
2. Click on the **New** button to create a new Avior Tax API configuration.
3. Fill in the required fields:
    - **Company**: Select the company that will use this API configuration.
    - **Username**: The username provided by Avior Tax Services.
    - **Password**: The password provided by Avior Tax Services.
    - **Service URL**: The URL provided by Avior Tax Services.
4. On the same form, you'll see that the **Token** field is empty and greyed out. This field will be automatically filled in once you click the **Login** button.
5. Click the **Login** button to authenticate with the Avior Tax Services API. If the authentication is successful, the **Token** field will be filled in with the authentication token.
6. You are also required to fill in extra details whose form can be accessed by clicking the **Details** tab. These details include:
    - **Seller Id**: The seller ID provided by Avior Tax Services. 
    - **Seller Location Id**: The seller location ID provided by Avior Tax Services.
    - **Seller State**: The state where the seller is located.
    - **Customer Entity Code**: The customer entity code provided by Avior Tax Services.
7. Click the **Save** button to save the configuration.

### Configure Taxes

By installing the connector, a default tax named **Avior** is created. This tax is already configured to use the Avior Tax Services API as well as being limited to the United States. You can create more taxes and configure them to use the Avior Tax Services API. You'll also notice that this default tax is set to 0.0000%. This is because Avior will dynamically determine the appropriate tax rate for the sale.

1. Navigate to **Accounting** > **Configuration** > **Accounting** > **Taxes**.
2. Click on the **New** button to create a new tax.
3. Fill in the required fields:
    - **Tax Name**: The name of the tax.
    - **Tax Type**: The type of tax. Note that only **Sales** is supported.
    - **Tax Computation**: The method used to compute the tax. Note that only **Percentage of Price** is supported.
    - **Amount**: The amount of the tax. This should be set to 0%. Avior will dynamically determine the appropriate tax rate.
    - **Is Avior Tax**: Check this box to indicate that this tax should use the Avior Tax Services API. This can be found under the **Advanced Options** tab.
    - **Country**: The country where the tax is applicable. Note that only **United States** is supported.
4. You can also (optionally) fill in the **Tax Group** field. The name of the tax group determines the name of the tax in the invoice.
5. Click the **Save** button to save the tax.

### Configure Fiscal Positions

By installing the connector, a default fiscal position named **Avior Tax Mapping (US)** is created. This fiscal position, when attached to an invoice, tells Avior to calculate the tax for that invoice. You can create more fiscal positions and configure them to use the Avior Tax Services API.

1. Navigate to **Accounting** > **Configuration** > **Accounting** > **Fiscal Positions**.
2. Click on the **New** button to create a new fiscal position.
3. Fill in the required fields:
    - **Fiscal Position Name**: The name of the fiscal position.
    - **Detect Automatically**: Check this box to automatically apply this fiscal position to an invoice based on the customer's address.
    - **Country**: The country where the fiscal position is applicable. Note that only **United States** is supported.
    - **Is Avior Tax**: Check this box to indicate that this fiscal position should use the Avior Tax Services API.
4. Click the **Save** button to save the fiscal position.

## How to use

1. Create a new customer or edit an existing customer. Fill in the customer's address and set the **County** field to the customer's county. Note that this field is an **optional** field.
2. Create a new invoice or edit an existing invoice (that's in a draft state).
3. Fill in the invoice lines and set the **Fiscal Position** field to the fiscal position that uses the Avior Tax Services API. However, if the **Detect Automatically** field is checked in the fiscal position, the fiscal position will be automatically applied based on the customer's address. This field can be found under the **Other Information** tab.
4. Click the **Compute Tax** button to calculate the tax for the invoice. If the tax is successfully calculated, the tax amount will be displayed in the **Tax** field.
