
Feature: Add products to shopping cart
  As a customer
  I want to add products to my shopping cart
  So that I can review the total amount before purchasing

  Scenario Outline: Add different quantities of a product to the cart
    Given the customer is on the product listing page
    When the customer searches for "Claw Hammer"
    And the customer opens the "Claw Hammer" product
    And the customer adds <quantity> units to the cart
    Then the shopping cart contains <quantity> units of the product
    And the line total equals the unit price multiplied by <quantity>

    Examples:
      | quantity |
      | 1        |
      | 3        |
