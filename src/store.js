import { create } from 'zustand';

// TECH-002 Validation: Zustand State Management
export const useValidationStore = create((set, get) => ({
  // Validation states
  validationTests: {
    reactApp: { status: 'success', message: 'React application running' },
    tailwindCSS: { status: 'testing', message: 'Checking responsive design...' },
    internationalization: { status: 'testing', message: 'Testing language switching...' },
    apiIntegration: { status: 'testing', message: 'Connecting to Flask auth service...' },
    routing: { status: 'testing', message: 'Testing navigation...' },
    stateManagement: { status: 'success', message: 'Zustand store initialized' }
  },

  // Update validation test status
  updateValidationTest: (testName, status, message) =>
    set((state) => ({
      validationTests: {
        ...state.validationTests,
        [testName]: { status, message }
      }
    })),

  // Authentication state
  auth: {
    isAuthenticated: false,
    user: null,
    token: null
  },

  // Login action
  login: async (email, password) => {
    set((state) => ({
      validationTests: {
        ...state.validationTests,
        apiIntegration: { status: 'testing', message: 'Attempting login...' }
      }
    }));

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        set((state) => ({
          auth: {
            isAuthenticated: true,
            user: { id: data.user_id, email: data.email },
            token: data.access_token
          },
          validationTests: {
            ...state.validationTests,
            apiIntegration: { status: 'success', message: 'Login successful! API integration working.' }
          }
        }));
        return { success: true, data };
      } else {
        const error = await response.json();
        set((state) => ({
          validationTests: {
            ...state.validationTests,
            apiIntegration: { status: 'failed', message: `Login failed: ${error.error}` }
          }
        }));
        return { success: false, error: error.error };
      }
    } catch (error) {
      set((state) => ({
        validationTests: {
          ...state.validationTests,
          apiIntegration: { status: 'failed', message: `Network error: ${error.message}` }
        }
      }));
      return { success: false, error: error.message };
    }
  },

  // Logout action
  logout: () =>
    set((state) => ({
      auth: {
        isAuthenticated: false,
        user: null,
        token: null
      },
      validationTests: {
        ...state.validationTests,
        apiIntegration: { status: 'testing', message: 'Ready for API testing...' }
      }
    })),

  // Shopping cart state
  cart: {
    items: [],
    total: 0
  },

  // Add item to cart
  addToCart: (product) =>
    set((state) => {
      const existingItem = state.cart.items.find(item => item.id === product.id);
      let newItems;
      
      if (existingItem) {
        newItems = state.cart.items.map(item =>
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        newItems = [...state.cart.items, { ...product, quantity: 1 }];
      }

      const total = newItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);

      return {
        cart: {
          items: newItems,
          total: total
        }
      };
    }),

  // Language state
  currentLanguage: 'en',
  
  // Change language
  changeLanguage: (language) =>
    set((state) => ({
      currentLanguage: language,
      validationTests: {
        ...state.validationTests,
        internationalization: { status: 'success', message: `Language changed to ${language}` }
      }
    }))
})); 