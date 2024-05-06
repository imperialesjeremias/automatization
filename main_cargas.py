import re, os
from playwright.async_api import async_playwright
from session.InitSession import InitSession
from cargas.cargas import extraer_texto

storage = InitSession()
data = extraer_texto('denuncia.pdf')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_context(storage_state=storage)
        page = await page.new_page()
        await page.goto("https://smartclaims.leverbox.com.ar/nuevosiniestro")

        await page.locator('.tt_Compaa').click()
        await page.locator('#null-97').click()
        await page.locator('.tt_Sucursal').click()
        await page.locator('#null-0', has_text='Buenos Aires').click()
        await page.get_by_placeholder('Número de póliza').fill(data['Referencia'])
        await page.locator('.tt_Estado').click()
        await page.locator('#null-0', has_text='Vigente').click()

        await page.locator('.fa-angle-right').click()

        await page.get_by_placeholder('Número de siniestro').fill(data['Denuncia de Siniestro'])
        await page.get_by_placeholder('Enter a location').first.fill(data['Detalle del Lugar'])
        await page.locator('span').get_by_text('Seleccionar un país').click()
        await page.get_by_role('option').first.click()
        await page.get_by_placeholder('Escriba aquí su descripción').first.fill(data['Descripción y consecuencias del siniestro'])

        await page.locator('.fa-angle-right').click()

        # Asegurado
        await page.locator('.tt_Tipodegestin').click()
        await page.locator('#null-3', has_text='RC Autos').click()
        await page.get_by_placeholder('Nombre').first.fill(data['Asegurado']['Nombre'])
        await page.get_by_placeholder('Cuit/Cuil').first.fill(data['Asegurado']['DNI'])
        await page.get_by_placeholder('Patente').first.fill(data['Asegurado']['Patente'])
        await page.get_by_placeholder('Marca').first.fill(data['Asegurado']['Marca'])
        
        await page.locator('button').get_by_text('Agregar involucrado').click()

        # Tercero
        await page.locator('.tt_Tipodegestin').nth(1).click()
        await page.locator('#null-3', has_text='RC Autos').nth(1).click()
        await page.get_by_placeholder('Nombre').nth(1).fill(data['Tercero']['Nombre'])
        await page.get_by_placeholder('Cuit/Cuil').nth(1).fill(data['Tercero']['DNI'])
        await page.get_by_placeholder('Patente').nth(1).fill(data['Tercero']['Patente'])
        await page.get_by_placeholder('Marca').nth(1).fill(data['Tercero']['Marca'])
        await page.get_by_placeholder('Email').nth(1).fill(data['Tercero']['Correo'])
        await page.get_by_placeholder('Telefono').nth(1).fill(data['Tercero']['Teléfono'])

        await page.wait_for_timeout(10000)
        await page.locator('button').get_by_text('Enviar').click()        
        await page.wait_for_timeout(10000)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())