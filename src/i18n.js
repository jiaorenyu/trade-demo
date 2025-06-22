import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// TECH-002 Validation: Internationalization setup
const resources = {
  en: {
    translation: {
      welcome: "Welcome to Global E-Commerce",
      navigation: {
        home: "Home",
        products: "Products",
        cart: "Cart",
        login: "Login"
      },
      auth: {
        login: "Login",
        register: "Register",
        email: "Email",
        password: "Password",
        loginSuccess: "Login successful!",
        loginFailed: "Login failed. Please try again."
      },
      products: {
        title: "Products",
        addToCart: "Add to Cart",
        price: "Price"
      },
      validation: {
        title: "TECH-002 Validation Dashboard",
        reactApp: "React Application",
        tailwindCSS: "Tailwind CSS Responsive Design",
        internationalization: "react-i18next Integration",
        apiIntegration: "Axios API Integration",
        routing: "React Router Navigation",
        stateManagement: "Zustand State Management",
        status: {
          success: "✅ Working",
          testing: "🧪 Testing...",
          failed: "❌ Failed"
        }
      }
    }
  },
  es: {
    translation: {
      welcome: "Bienvenido al Comercio Electrónico Global",
      navigation: {
        home: "Inicio",
        products: "Productos",
        cart: "Carrito",
        login: "Iniciar Sesión"
      },
      auth: {
        login: "Iniciar Sesión",
        register: "Registrarse",
        email: "Correo Electrónico",
        password: "Contraseña",
        loginSuccess: "¡Inicio de sesión exitoso!",
        loginFailed: "Error en el inicio de sesión. Inténtalo de nuevo."
      },
      products: {
        title: "Productos",
        addToCart: "Agregar al Carrito",
        price: "Precio"
      },
      validation: {
        title: "Panel de Validación TECH-002",
        reactApp: "Aplicación React",
        tailwindCSS: "Diseño Responsivo con Tailwind CSS",
        internationalization: "Integración react-i18next",
        apiIntegration: "Integración API con Axios",
        routing: "Navegación con React Router",
        stateManagement: "Gestión de Estado con Zustand",
        status: {
          success: "✅ Funcionando",
          testing: "🧪 Probando...",
          failed: "❌ Fallido"
        }
      }
    }
  },
  zh: {
    translation: {
      welcome: "欢迎来到全球电子商务",
      navigation: {
        home: "首页",
        products: "产品",
        cart: "购物车",
        login: "登录"
      },
      auth: {
        login: "登录",
        register: "注册",
        email: "邮箱",
        password: "密码",
        loginSuccess: "登录成功！",
        loginFailed: "登录失败，请重试。"
      },
      products: {
        title: "产品",
        addToCart: "加入购物车",
        price: "价格"
      },
      validation: {
        title: "TECH-002 验证仪表板",
        reactApp: "React 应用程序",
        tailwindCSS: "Tailwind CSS 响应式设计",
        internationalization: "react-i18next 集成",
        apiIntegration: "Axios API 集成",
        routing: "React Router 导航",
        stateManagement: "Zustand 状态管理",
        status: {
          success: "✅ 工作中",
          testing: "🧪 测试中...",
          failed: "❌ 失败"
        }
      }
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en', // default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // react already escapes values
    }
  });

export default i18n; 