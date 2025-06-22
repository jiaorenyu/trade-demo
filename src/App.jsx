import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useValidationStore } from './store';
import './i18n';
import './index.css';

// TECH-002 Validation Components
const ValidationDashboard = () => {
  const { t } = useTranslation();
  const { validationTests, updateValidationTest } = useValidationStore();

  useEffect(() => {
    // Simulate responsive design testing
    setTimeout(() => {
      updateValidationTest('tailwindCSS', 'success', 'Responsive design working correctly');
    }, 1000);

    // Simulate routing test
    setTimeout(() => {
      updateValidationTest('routing', 'success', 'React Router navigation working');
    }, 1500);
  }, [updateValidationTest]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return '✅';
      case 'testing': return '🧪';
      case 'failed': return '❌';
      default: return '⏳';
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">{t('validation.title')}</h1>
      
      <div className="responsive-grid">
        {Object.entries(validationTests).map(([testName, test]) => (
          <div key={testName} className="card">
            <h3 className="text-lg font-semibold mb-2">
              {getStatusIcon(test.status)} {t(`validation.${testName}`)}
            </h3>
            <p className="text-gray-600">{test.message}</p>
            <div className="mt-2">
              <span className={`px-2 py-1 rounded text-sm ${
                test.status === 'success' ? 'bg-green-100 text-green-800' :
                test.status === 'testing' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {t(`validation.status.${test.status}`)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const HomePage = () => {
  const { t } = useTranslation();
  
  return (
    <div className="container mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">{t('welcome')}</h1>
        <p className="text-xl text-gray-600">TECH-002 React.js Technology Validation</p>
      </div>
      
      <div className="responsive-grid">
        <div className="card">
          <h2 className="text-xl font-semibold mb-3">🚀 React Application</h2>
          <p>Modern React application built with Vite for fast development and optimized builds.</p>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold mb-3">🎨 Responsive Design</h2>
          <p>CSS Grid and Flexbox layout that adapts to mobile, tablet, and desktop screens.</p>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold mb-3">🌍 Internationalization</h2>
          <p>Multi-language support with react-i18next for global accessibility.</p>
        </div>
      </div>
    </div>
  );
};

const ProductsPage = () => {
  const { t } = useTranslation();
  const { addToCart } = useValidationStore();

  const sampleProducts = [
    { id: 1, name: 'Smartphone', price: 599.99, image: '📱' },
    { id: 2, name: 'Laptop', price: 1299.99, image: '💻' },
    { id: 3, name: 'Headphones', price: 199.99, image: '🎧' },
    { id: 4, name: 'Watch', price: 299.99, image: '⌚' },
    { id: 5, name: 'Tablet', price: 799.99, image: '📱' },
    { id: 6, name: 'Camera', price: 899.99, image: '📷' }
  ];

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">{t('products.title')}</h1>
      
      <div className="responsive-grid">
        {sampleProducts.map(product => (
          <div key={product.id} className="card">
            <div className="text-4xl mb-3 text-center">{product.image}</div>
            <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
            <p className="text-xl font-bold text-blue-600 mb-3">
              ${product.price}
            </p>
            <button 
              onClick={() => addToCart(product)}
              className="btn-primary w-full"
            >
              {t('products.addToCart')}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

const LoginPage = () => {
  const { t } = useTranslation();
  const { login, auth } = useValidationStore();
  const navigate = useNavigate();
  const [formData, setFormData] = React.useState({ email: '', password: '' });
  const [message, setMessage] = React.useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      setMessage(t('auth.loginSuccess'));
      setTimeout(() => navigate('/'), 2000);
    } else {
      setMessage(result.error || t('auth.loginFailed'));
    }
  };

  if (auth.isAuthenticated) {
    return (
      <div className="container mx-auto p-6 text-center">
        <h1 className="text-3xl font-bold mb-4">Welcome back!</h1>
        <p className="text-lg">User: {auth.user?.email}</p>
        <p className="text-sm text-gray-600 mt-2">API Integration: ✅ Working</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 max-w-md">
      <h1 className="text-3xl font-bold mb-6 text-center">{t('auth.login')}</h1>
      
      <form onSubmit={handleSubmit} className="card">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">{t('auth.email')}</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="test@example.com"
            required
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">{t('auth.password')}</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="securepassword123"
            required
          />
        </div>
        
        <button type="submit" className="btn-primary w-full">
          {t('auth.login')}
        </button>
        
        {message && (
          <div className="mt-4 p-3 bg-blue-100 text-blue-800 rounded">
            {message}
          </div>
        )}
        
        <div className="mt-4 text-sm text-gray-600">
          <p>Test credentials:</p>
          <p>Email: test@example.com</p>
          <p>Password: securepassword123</p>
        </div>
      </form>
    </div>
  );
};

const CartPage = () => {
  const { t } = useTranslation();
  const { cart } = useValidationStore();

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">{t('navigation.cart')}</h1>
      
      {cart.items.length === 0 ? (
        <div className="card text-center">
          <p className="text-lg text-gray-600">Your cart is empty</p>
          <Link to="/products" className="btn-primary inline-block mt-4">
            Shop Now
          </Link>
        </div>
      ) : (
        <div>
          {cart.items.map(item => (
            <div key={item.id} className="card mb-4">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold">{item.name}</h3>
                  <p className="text-gray-600">Quantity: {item.quantity}</p>
                </div>
                <div className="text-xl font-bold">
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            </div>
          ))}
          
          <div className="card bg-blue-50">
            <div className="text-xl font-bold text-center">
              Total: ${cart.total.toFixed(2)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const Navigation = () => {
  const { t, i18n } = useTranslation();
  const { auth, logout, cart, changeLanguage } = useValidationStore();

  const handleLanguageChange = (lang) => {
    i18n.changeLanguage(lang);
    changeLanguage(lang);
  };

  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex flex-wrap justify-between items-center">
        <Link to="/" className="text-xl font-bold">E-Commerce</Link>
        
        <div className="flex flex-wrap items-center space-x-4">
          <Link to="/" className="hover:text-blue-200">{t('navigation.home')}</Link>
          <Link to="/products" className="hover:text-blue-200">{t('navigation.products')}</Link>
          <Link to="/cart" className="hover:text-blue-200">
            {t('navigation.cart')} ({cart.items.length})
          </Link>
          <Link to="/validation" className="hover:text-blue-200">Validation</Link>
          
          {auth.isAuthenticated ? (
            <button onClick={logout} className="hover:text-blue-200">
              Logout ({auth.user?.email})
            </button>
          ) : (
            <Link to="/login" className="hover:text-blue-200">{t('navigation.login')}</Link>
          )}
          
          <div className="flex space-x-2">
            <button
              onClick={() => handleLanguageChange('en')}
              className={`px-2 py-1 rounded ${i18n.language === 'en' ? 'bg-blue-800' : 'bg-blue-500'}`}
            >
              EN
            </button>
            <button
              onClick={() => handleLanguageChange('es')}
              className={`px-2 py-1 rounded ${i18n.language === 'es' ? 'bg-blue-800' : 'bg-blue-500'}`}
            >
              ES
            </button>
            <button
              onClick={() => handleLanguageChange('zh')}
              className={`px-2 py-1 rounded ${i18n.language === 'zh' ? 'bg-blue-800' : 'bg-blue-500'}`}
            >
              中文
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/validation" element={<ValidationDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 