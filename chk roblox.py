from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from faker import Faker
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurações
PRODUCT_URL = "https://www.gsgames.com.br/robux-500-roblox"
NUM_SIMULATIONS = 3

# Dados de teste
fake = Faker('pt_BR')
test_cards = [
    {"number": "4111 1111 1111 1111", "type": "Visa"},
    {"number": "5500 0000 0000 0004", "type": "Mastercard"},
    {"number": "3400 0000 0000 009", "type": "American Express"}
]

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def simulate_purchase(driver, card_data):
    try:
        logger.info(f"Iniciando simulação com cartão {card_data['type']}")
        
        # 1. Acessar a página do produto
        driver.get(PRODUCT_URL)
        logger.info("Página do produto carregada")
        time.sleep(random.uniform(3, 5))
        
        # 2. Aceitar cookies (com várias tentativas)
        try:
            cookie_selectors = [
                (By.ID, "onetrust-accept-btn-handler"),
                (By.CLASS_NAME, "ot-btn"),
                (By.XPATH, "//button[contains(text(), 'Aceitar')]")
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    cookie_btn.click()
                    logger.info("Cookies aceitos")
                    time.sleep(1)
                    break
                except:
                    continue
        except Exception as e:
            logger.warning(f"Botão de cookies não encontrado: {str(e)}")
        
        # 3. Localizar e clicar no botão de compra com múltiplas estratégias
        add_button = None
        add_button_selectors = [
            (By.CSS_SELECTOR, "a.botao.botao-comprar.principal.grande"), # Novo e mais preciso
            (By.XPATH, "//a[contains(@class, 'botao-comprar') and contains(., 'Comprar')]"), # Novo e mais preciso
            (By.PARTIAL_LINK_TEXT, "Comprar"), # Novo
            (By.XPATH, "//button[contains(., 'Adicionar')]"),
            (By.ID, "product-addtocart-button"),
            (By.CLASS_NAME, "botao-comprar") # Simplificado
        ]
        
        for selector in add_button_selectors:
            try:
                add_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(selector)
                )
                logger.info(f"Botão encontrado com seletor: {selector}")
                break
            except:
                continue
        
        if not add_button:
            logger.error("Nenhum seletor de botão de compra funcionou")
            return False
        
        # Role até o elemento e clique
        ActionChains(driver).move_to_element(add_button).click().perform()
        logger.info("Produto adicionado ao carrinho")
        time.sleep(random.uniform(2, 4))
        
        # 4. Ir para o carrinho
        try:
            cart_selectors = [
                (By.CSS_SELECTOR, "a.action.showcart"),
                (By.CSS_SELECTOR, "a.cart-link"),
                (By.XPATH, "//a[contains(., 'Carrinho')]")
            ]
            
            for selector in cart_selectors:
                try:
                    cart_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(selector)
                    )
                    cart_btn.click()
                    logger.info("Carrinho acessado")
                    break
                except:
                    continue
            else:
                driver.get("https://www.gsgames.com.br/carrinho/index/")
                logger.info("Acessado carrinho via URL direta")
                
            time.sleep(random.uniform(3, 5))
        except Exception as e:
            logger.error(f"Erro ao acessar carrinho: {str(e)}")
            return False
        
        # 5. Iniciar checkout
        try:
            checkout_selectors = [
                (By.CSS_SELECTOR, "button.botao.principal.grande")
            ]
            
            for selector in checkout_selectors:
                try:
                    checkout_btn = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable(selector)
                    )
                    checkout_btn.click()
                    logger.info("Checkout iniciado")
                    time.sleep(random.uniform(4, 6))
                    break
                except:
                    continue
            else:
                logger.error("Botão de checkout não encontrado")
                return False
        except Exception as e:
            logger.error(f"Erro ao iniciar checkout: {str(e)}")
            return False
        
        # 6. Preencher informações de entrega
        logger.info("Preenchendo informações de entrega...")
        try:
            # Email
            email_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "customer-email"))
            )
            email_field.send_keys(fake.email())
            time.sleep(random.uniform(0.5, 1.5))
            
            # Nome completo (pode estar dividido em primeiro/último nome)
            try:
                driver.find_element(By.NAME, "firstname").send_keys(fake.first_name())
                driver.find_element(By.NAME, "lastname").send_keys(fake.last_name())
            except:
                driver.find_element(By.NAME, "fullname").send_keys(fake.name())
            
            # CPF
            driver.find_element(By.NAME, "taxvat").send_keys(fake.cpf())
            time.sleep(random.uniform(0.5, 1))
            
            # Telefone
            driver.find_element(By.NAME, "telephone").send_keys(fake.cellphone_number().replace(' ', '').replace('-', ''))
            time.sleep(random.uniform(0.5, 1))
            
            # CEP
            cep_field = driver.find_element(By.NAME, "postcode")
            cep_field.clear()
            cep_field.send_keys(fake.postcode())
            time.sleep(random.uniform(1, 2))
            
            # Buscar CEP
            try:
                driver.find_element(By.XPATH, "//button[contains(., 'Buscar CEP')]").click()
                time.sleep(random.uniform(3, 5))
            except:
                logger.warning("Botão 'Buscar CEP' não encontrado")
            
            # Preencher número (caso não preenchido automaticamente)
            try:
                number_field = driver.find_element(By.NAME, "street_1")
                if number_field.get_attribute("value") == "":
                    number_field.send_keys(str(random.randint(1, 9999)))
                    time.sleep(0.5)
            except:
                pass
            
            # Continuar para pagamento
            continue_buttons = [
                (By.XPATH, "//button[contains(., 'Continuar')]"),
                (By.CSS_SELECTOR, "button.continue")
            ]
            
            for selector in continue_buttons:
                try:
                    driver.find_element(*selector).click()
                    logger.info("Informações de entrega preenchidas")
                    time.sleep(random.uniform(4, 6))
                    break
                except:
                    continue
        except Exception as e:
            logger.error(f"Erro no formulário de entrega: {str(e)}")
            return False
        
        # 7. Selecionar método de pagamento
        try:
            payment_method_selectors = [
                (By.XPATH, "//label[contains(., 'Cartão de Crédito')]"),
                (By.XPATH, "//input[@value='credit_card']/..")
            ]
            
            for selector in payment_method_selectors:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(selector)
                    ).click()
                    logger.info("Cartão de crédito selecionado")
                    time.sleep(random.uniform(2, 3))
                    break
                except:
                    continue
        except Exception as e:
            logger.error(f"Não foi possível selecionar cartão de crédito: {str(e)}")
            return False
        
        # 8. Preencher dados do cartão
        logger.info("Preenchendo dados do cartão...")
        try:
            # Número do cartão
            card_number_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "card[number]"))
            )
            card_number_field.send_keys(card_data["number"])
            time.sleep(random.uniform(0.5, 1.5))
            
            # Nome no cartão
            driver.find_element(By.NAME, "card[holder]").send_keys(fake.name())
            time.sleep(random.uniform(0.3, 0.8))
            
            # Validade
            driver.find_element(By.NAME, "card[exp_month]").send_keys(f"{random.randint(1,12):02d}")
            driver.find_element(By.NAME, "card[exp_year]").send_keys(f"{random.randint(2025,2030)}")
            time.sleep(random.uniform(0.5, 1))
            
            # CVV
            driver.find_element(By.NAME, "card[cvv]").send_keys(f"{random.randint(100,999)}")
            time.sleep(random.uniform(0.5, 1))
            
            # Parcelamento
            try:
                installments = Select(driver.find_element(By.NAME, "card[installments]"))
                installments.select_by_index(random.randint(1, min(6, len(installments.options)-1)))
                time.sleep(1)
            except:
                logger.warning("Seletor de parcelas não encontrado")
            
            logger.info(f"Dados do cartão {card_data['type']} preenchidos")
            
            # 9. Finalizar compra (SIMULAÇÃO - não clicar realmente)
            logger.info("Simulação completa - Transação não foi realmente finalizada")
            logger.info("Este é um exercício educacional sem transação real")
            
            return True
        
        except Exception as e:
            logger.error(f"Erro no formulário de pagamento: {str(e)}")
            return False
        
    except Exception as e:
        logger.error(f"Erro geral na simulação: {str(e)}")
        return False

def main():
    driver = setup_driver()
    
    try:
        logger.info(f"Iniciando {NUM_SIMULATIONS} simulações de compra")
        
        for i in range(NUM_SIMULATIONS):
            logger.info(f"\n=== SIMULAÇÃO {i+1}/{NUM_SIMULATIONS} ===")
            
            # Selecionar cartão
            card = random.choice(test_cards)
            success = simulate_purchase(driver, card)
            
            # Limpar estado entre simulações
            driver.delete_all_cookies()
            driver.execute_script("localStorage.clear();")
            driver.get("about:blank")
            time.sleep(2)
            
            # Pausa entre simulações
            if i < NUM_SIMULATIONS - 1:
                wait_time = random.randint(15, 30)
                logger.info(f"Próxima simulação em {wait_time} segundos...")
                time.sleep(wait_time)
        
        logger.info("Todas as simulações foram concluídas!")
    
    except KeyboardInterrupt:
        logger.info("Operação interrompida pelo usuário")
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
    finally:
        driver.quit()
        logger.info("Navegador fechado")

if __name__ == "__main__":
    main()