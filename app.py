import re, os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from session.InitSession import InitSession

storage = InitSession()
siniestros = [
84752,
89858,
89447,
88728,
88700,
83198,
83738,
87112,
89522,
87237,
88629,
90045,
88345,
89449,
87612,
88757,
89160,
86292,
89540,
86782,
87868,
86674,
90226,
61187,
85086,
88771
]

async def main():
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_context(storage_state=storage)
        page = await page.new_page()
        await page.goto("https://smartclaims.leverbox.com.ar/siniestros")

        await page.wait_for_load_state("networkidle")
        
        await page.wait_for_selector('button:has-text("Filtros")')
        await page.click('button:has-text("Filtros")')
        
        
        await page.wait_for_selector('button:has-text("Buscar multiple")')
        await page.click('button:has-text("Buscar multiple")')
        print("Buscar multiple clicked")
        
        await page.locator('.tt_Seleccionarcampo').click()
        await page.locator('span').get_by_text('Id de solicitud').click()

        

        for siniestro in siniestros.replace(',', '\n').split:
            siniestros_input = '\n'.join(siniestro)
            await page.get_by_placeholder('Ingrese parametros separados por un espacio').fill(siniestros_input)


        await page.locator('.btn-succes').get_by_text('Buscar').click()
        

        await page.wait_for_timeout(10000)


        await browser.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())