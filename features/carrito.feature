Feature: Compra de productos

  Scenario: Usuario Jason compra una pera
    Given que estoy en la página de login
    When ingreso usuario "jason" y clave "1234"
    And presiono el botón de ingresar
    When selecciono el producto "pera"
