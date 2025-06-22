import React, { useState, useEffect } from 'react'
import './App.css'

// Header Component
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header style={{ backgroundColor: 'white', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', position: 'sticky', top: 0, zIndex: 50 }}>
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ fontSize: '2rem' }}>🛒</div>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>E-Commerce Platform</h1>
          </div>
          
          {/* Desktop Navigation */}
          <nav style={{ display: 'none', gap: '2rem' }} className="desktop-nav">
            <a href="#" style={{ color: '#374151', fontWeight: '500', textDecoration: 'none', transition: 'color 0.2s' }}>Home</a>
            <a href="#" style={{ color: '#374151', fontWeight: '500', textDecoration: 'none', transition: 'color 0.2s' }}>Products</a>
            <a href="#" style={{ color: '#374151', fontWeight: '500', textDecoration: 'none', transition: 'color 0.2s' }}>Categories</a>
            <a href="#" style={{ color: '#374151', fontWeight: '500', textDecoration: 'none', transition: 'color 0.2s' }}>About</a>
            <a href="#" style={{ color: '#374151', fontWeight: '500', textDecoration: 'none', transition: 'color 0.2s' }}>Contact</a>
          </nav>
          
          {/* Action Buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button style={{ color: '#374151', padding: '0.5rem', borderRadius: '0.5rem', border: 'none', background: 'transparent', cursor: 'pointer' }}>
              🔍
            </button>
            <button style={{ color: '#374151', padding: '0.5rem', borderRadius: '0.5rem', border: 'none', background: 'transparent', cursor: 'pointer', position: 'relative' }}>
              🛒
              <span style={{ position: 'absolute', top: '-0.25rem', right: '-0.25rem', backgroundColor: '#2563eb', color: 'white', fontSize: '0.75rem', borderRadius: '50%', width: '1.25rem', height: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>0</span>
            </button>
            <button className="btn-primary">
              Login
            </button>
            
            {/* Mobile menu button */}
            <button 
              style={{ padding: '0.5rem', borderRadius: '0.5rem', border: 'none', background: 'transparent', cursor: 'pointer' }}
              className="mobile-menu-btn"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              ☰
            </button>
          </div>
        </div>
        
        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div style={{ padding: '1rem 0', borderTop: '1px solid #e5e7eb' }} className="animate-fade-in mobile-nav">
            <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <a href="#" style={{ color: '#374151', padding: '0.5rem 0', fontWeight: '500', textDecoration: 'none' }}>Home</a>
              <a href="#" style={{ color: '#374151', padding: '0.5rem 0', fontWeight: '500', textDecoration: 'none' }}>Products</a>
              <a href="#" style={{ color: '#374151', padding: '0.5rem 0', fontWeight: '500', textDecoration: 'none' }}>Categories</a>
              <a href="#" style={{ color: '#374151', padding: '0.5rem 0', fontWeight: '500', textDecoration: 'none' }}>About</a>
              <a href="#" style={{ color: '#374151', padding: '0.5rem 0', fontWeight: '500', textDecoration: 'none' }}>Contact</a>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}

// Hero Section Component
const HeroSection = () => {
  return (
    <section className="gradient-hero" style={{ color: 'white', position: 'relative', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0, 0, 0, 0.2)' }}></div>
      <div className="container" style={{ position: 'relative', zIndex: 10, padding: '5rem 1rem' }}>
        <div style={{ textAlign: 'center' }} className="animate-fade-in">
          <h2 style={{ fontSize: '3rem', fontWeight: 'bold', marginBottom: '1.5rem', textShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
            Welcome to Our Store
          </h2>
          <p style={{ fontSize: '1.25rem', marginBottom: '2rem', maxWidth: '48rem', margin: '0 auto 2rem', opacity: 0.9 }}>
            Discover amazing products at unbeatable prices. Shop with confidence and enjoy fast, secure delivery.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', justifyContent: 'center', alignItems: 'center' }}>
            <button style={{ backgroundColor: 'white', color: '#2563eb', padding: '1rem 2rem', borderRadius: '0.5rem', fontWeight: '600', border: 'none', cursor: 'pointer', fontSize: '1rem', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', transition: 'all 0.2s' }}>
              Shop Now
            </button>
            <button className="btn-secondary" style={{ color: 'white', borderColor: 'white' }}>
              Learn More
            </button>
          </div>
        </div>
      </div>
      
      {/* Decorative elements */}
      <div style={{ position: 'absolute', top: '2.5rem', left: '2.5rem', width: '5rem', height: '5rem', backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: '50%' }} className="animate-pulse-slow"></div>
      <div style={{ position: 'absolute', bottom: '2.5rem', right: '2.5rem', width: '8rem', height: '8rem', backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: '50%', animationDelay: '1s' }} className="animate-pulse-slow"></div>
    </section>
  )
}

// Product Card Component
const ProductCard = ({ product, index }) => {
  return (
    <div className="card animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
      <div style={{ height: '12rem', background: 'linear-gradient(135deg, #eff6ff 0%, #f3e8ff 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ fontSize: '4rem', transition: 'transform 0.2s', cursor: 'pointer' }}>{product.emoji}</span>
      </div>
      <div style={{ padding: '1.5rem' }}>
        <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '0.5rem' }}>{product.name}</h3>
        <p style={{ color: '#6b7280', marginBottom: '1rem', lineHeight: '1.6' }}>{product.description}</p>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#2563eb' }}>${product.price}</span>
          <button style={{ backgroundColor: '#2563eb', color: 'white', padding: '0.5rem 1rem', borderRadius: '0.5rem', border: 'none', cursor: 'pointer', fontWeight: '500', transition: 'all 0.2s', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  )
}

// Featured Products Section
const FeaturedProducts = () => {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call to fetch products
    setTimeout(() => {
      const mockProducts = [
        {
          id: 1,
          name: "Wireless Headphones",
          description: "Premium sound quality with active noise cancellation technology",
          price: 199.99,
          emoji: "🎧"
        },
        {
          id: 2,
          name: "Smart Watch",
          description: "Track your fitness goals and stay connected on the go",
          price: 299.99,
          emoji: "⌚"
        },
        {
          id: 3,
          name: "Laptop Computer",
          description: "High-performance laptop for work, gaming, and creativity",
          price: 999.99,
          emoji: "💻"
        },
        {
          id: 4,
          name: "Smartphone",
          description: "Latest flagship device with cutting-edge camera technology",
          price: 699.99,
          emoji: "📱"
        },
        {
          id: 5,
          name: "Gaming Console",
          description: "Next-generation gaming with stunning 4K graphics",
          price: 499.99,
          emoji: "🎮"
        },
        {
          id: 6,
          name: "Wireless Speaker",
          description: "360-degree premium audio for your home entertainment",
          price: 149.99,
          emoji: "🔊"
        }
      ]
      setProducts(mockProducts)
      setLoading(false)
    }, 1500)
  }, [])

  return (
    <section style={{ padding: '4rem 0', backgroundColor: '#f9fafb' }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '3rem' }} className="animate-fade-in">
          <h2 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '1rem' }}>
            Featured Products
          </h2>
          <p style={{ fontSize: '1.25rem', color: '#6b7280', maxWidth: '32rem', margin: '0 auto' }}>
            Discover our most popular items, carefully selected for quality and value
          </p>
          <div style={{ width: '6rem', height: '0.25rem', backgroundColor: '#2563eb', margin: '1.5rem auto', borderRadius: '0.125rem' }}></div>
        </div>

        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '4rem 0' }}>
            <div className="animate-spin" style={{ width: '4rem', height: '4rem', borderRadius: '50%', border: '4px solid #f3f4f6', borderTopColor: '#2563eb' }}></div>
            <span style={{ marginLeft: '1rem', fontSize: '1.25rem', color: '#6b7280', fontWeight: '500' }}>Loading amazing products...</span>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
            {products.map((product, index) => (
              <ProductCard key={product.id} product={product} index={index} />
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

// Stats Section
const StatsSection = () => {
  const stats = [
    { number: "10K+", label: "Happy Customers", emoji: "😊" },
    { number: "5K+", label: "Products", emoji: "📦" },
    { number: "50+", label: "Countries", emoji: "🌍" },
    { number: "24/7", label: "Support", emoji: "🛠️" }
  ]

  return (
    <section style={{ padding: '4rem 0', backgroundColor: 'white' }}>
      <div className="container">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem' }}>
          {stats.map((stat, index) => (
            <div key={index} style={{ textAlign: 'center' }} className="animate-fade-in" data-delay={index * 200}>
              <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>{stat.emoji}</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2563eb', marginBottom: '0.25rem' }}>{stat.number}</div>
              <div style={{ color: '#6b7280', fontWeight: '500' }}>{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

// Footer Component
const Footer = () => {
  return (
    <footer style={{ backgroundColor: '#1f2937', color: 'white' }}>
      <div className="container" style={{ padding: '3rem 0' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
          <div className="animate-fade-in">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <span style={{ fontSize: '1.5rem' }}>🛒</span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>E-Commerce Platform</h3>
            </div>
            <p style={{ color: '#9ca3af', lineHeight: '1.6' }}>
              Your trusted online marketplace for quality products and exceptional service. Shop with confidence!
            </p>
          </div>
          <div className="animate-fade-in">
            <h4 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>Quick Links</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>About Us</a></li>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>Contact</a></li>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>FAQ</a></li>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>Support</a></li>
            </ul>
          </div>
          <div className="animate-fade-in">
            <h4 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>Categories</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>Electronics</a></li>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>Fashion</a></li>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>Home & Garden</a></li>
              <li><a href="#" style={{ color: '#9ca3af', textDecoration: 'none', transition: 'color 0.2s' }}>Sports</a></li>
            </ul>
          </div>
          <div className="animate-fade-in">
            <h4 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>Follow Us</h4>
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
              <a href="#" style={{ color: '#9ca3af', fontSize: '1.5rem', textDecoration: 'none', transition: 'color 0.2s' }}>📘</a>
              <a href="#" style={{ color: '#9ca3af', fontSize: '1.5rem', textDecoration: 'none', transition: 'color 0.2s' }}>🐦</a>
              <a href="#" style={{ color: '#9ca3af', fontSize: '1.5rem', textDecoration: 'none', transition: 'color 0.2s' }}>📷</a>
              <a href="#" style={{ color: '#9ca3af', fontSize: '1.5rem', textDecoration: 'none', transition: 'color 0.2s' }}>💼</a>
            </div>
            <div>
              <h5 style={{ fontWeight: '600', marginBottom: '0.5rem', fontSize: '1rem' }}>Newsletter</h5>
              <div style={{ display: 'flex' }}>
                <input 
                  type="email" 
                  placeholder="Your email" 
                  style={{ backgroundColor: '#374151', color: 'white', padding: '0.75rem', borderRadius: '0.5rem 0 0 0.5rem', border: 'none', flex: 1 }}
                />
                <button style={{ backgroundColor: '#2563eb', padding: '0.75rem 1rem', borderRadius: '0 0.5rem 0.5rem 0', border: 'none', color: 'white', cursor: 'pointer', transition: 'background-color 0.2s' }}>
                  ✉️
                </button>
              </div>
            </div>
          </div>
        </div>
        <div style={{ borderTop: '1px solid #374151', marginTop: '2rem', paddingTop: '2rem', textAlign: 'center', color: '#9ca3af' }}>
          <p style={{ margin: 0 }}>&copy; 2024 E-Commerce Platform. All rights reserved. Built with ❤️</p>
        </div>
      </div>
    </footer>
  )
}

// Main App Component
function App() {
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Test API connectivity
    const testConnection = async () => {
      try {
        const response = await fetch('http://localhost:5001/health')
        if (response.ok) {
          setIsConnected(true)
        }
      } catch (error) {
        console.log('Backend not connected yet:', error)
      }
    }

    testConnection()
    const interval = setInterval(testConnection, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ minHeight: '100vh', backgroundColor: 'white' }}>
      

      {/* Main Application */}
      <Header />
      <HeroSection />
      <StatsSection />
      <FeaturedProducts />
      <Footer />
    </div>
  )
}

export default App
