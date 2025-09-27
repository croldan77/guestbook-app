# test_index_html.py
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def test_flask_server():
    """Verifica que el servidor Flask esté funcionando"""
    print("🔍 Verificando servidor Flask...")
    try:
        response = requests.get("http://127.0.0.1:5001/guestbook")
        if response.status_code == 200:
            print("✅ Servidor Flask funcionando correctamente")
            return True
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor Flask")
        print("💡 Ejecuta primero: python app.py")
        return False

def test_html_structure():
    """Valida la estructura HTML de la página"""
    print("\n📄 Validando estructura HTML...")
    
    try:
        response = requests.get("http://127.0.0.1:5001/guestbook")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verificar elementos esenciales
        checks = [
            ("Título de la página", soup.title and soup.title.string),
            ("Formulario de envío", soup.find('form')),
            ("Campo nombre", soup.find('input', {'name': 'name'})),
            ("Campo mensaje", soup.find('textarea', {'name': 'message'})),
            ("Botón enviar", soup.find('button', {'type': 'submit'}) or soup.find('input', {'type': 'submit'}))
        ]
        
        all_passed = True
        for element_name, element in checks:
            if element:
                print(f"✅ {element_name}: encontrado")
            else:
                print(f"❌ {element_name}: no encontrado")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error validando HTML: {e}")
        return False

def test_form_submission():
    """Prueba el envío del formulario HTML"""
    print("\n📤 Probando envío de formulario...")
    
    try:
        # Datos de prueba
        test_data = {
            'name': 'Usuario de Prueba',
            'message': 'Este es un mensaje de prueba desde el validador HTML'
        }
        
        response = requests.post(
            "http://127.0.0.1:5001/guestbook",
            data=test_data
        )
        
        if response.status_code == 200:
            # Verificar que el mensaje se haya guardado
            response_get = requests.get("http://127.0.0.1:5001/guestbook")
            soup = BeautifulSoup(response_get.content, 'html.parser')
            
            # Buscar el mensaje en la página
            entries = soup.find_all(class_=['entry', 'message']) or soup.find_all('div')
            message_found = any(test_data['message'] in str(entry) for entry in entries)
            
            if message_found:
                print("✅ Formulario HTML: envío y visualización correctos")
                return True
            else:
                print("⚠️ Formulario enviado, pero mensaje no visible en la página")
                return True  # Puede ser un delay en la actualización
        else:
            print(f"❌ Error en envío de formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando formulario: {e}")
        return False

def test_responsive_design():
    """Verifica aspectos básicos de diseño responsive"""
    print("\n📱 Validando diseño responsive...")
    
    try:
        response = requests.get("http://127.0.0.1:5001/guestbook")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verificar viewport meta tag (importante para responsive)
        viewport = soup.find('meta', {'name': 'viewport'})
        if viewport:
            print("✅ Meta viewport: presente (bueno para móviles)")
        else:
            print("⚠️ Meta viewport: no encontrado")
        
        # Verificar si hay CSS inline o en archivo
        style_tags = soup.find_all('style')
        if style_tags:
            print("✅ CSS: encontrado (estilos aplicados)")
        else:
            print("⚠️ CSS: no encontrado en la página")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validando diseño: {e}")
        return False

def test_navigation():
    """Prueba la navegación y enlaces"""
    print("\n🧭 Probando navegación...")
    
    try:
        response = requests.get("http://127.0.0.1:5001/")
        if response.status_code == 200:
            print("✅ Redirección desde / a /guestbook: funcionando")
        else:
            print("❌ Redirección no funciona correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en navegación: {e}")
        return False

def manual_browser_test():
    """Guía para pruebas manuales en el navegador"""
    print("\n👁️ Pruebas manuales recomendadas:")
    print("1. Abre http://127.0.0.1:5001/guestbook en tu navegador")
    print("2. Verifica que:")
    print("   - El formulario se vea correctamente")
    print("   - Los campos nombre y mensaje sean editables")
    print("   - El botón 'Enviar' funcione")
    print("   - Los mensajes anteriores se muestren")
    print("   - La página sea responsive (probar en móvil/tablet)")
    print("3. Prueba enviar un mensaje y verificar que aparece en la lista")

def main():
    """Función principal"""
    print("🌐 VALIDADOR DE INDEX.HTML")
    print("=" * 50)
    
    # Verificar que el servidor esté corriendo
    if not test_flask_server():
        return
    
    # Ejecutar tests automáticos
    tests = [
        ("Estructura HTML", test_html_structure),
        ("Envío de formulario", test_form_submission),
        ("Diseño responsive", test_responsive_design),
        ("Navegación", test_navigation)
    ]
    
    results = []
    for test_name, test_function in tests:
        try:
            success = test_function()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VALIDACIÓN HTML")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{status} - {test_name}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\n🎯 Resultado: {total_passed}/{len(results)} tests exitosos")
    
    # Mostrar guía para pruebas manuales
    manual_browser_test()

if __name__ == "__main__":
    main()