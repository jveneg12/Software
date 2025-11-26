Feature: Eliminación de productos

  Scenario: Admin elimina un producto
    Given que estoy en la página de login
    When ingreso usuario "admin" y clave "1234"
    And presiono el botón de ingresar
    Then debería ver la página de menú
    When selecciono la opción de productos
    Then debería ver la página de productos
    When elimino el producto con ID "6"
