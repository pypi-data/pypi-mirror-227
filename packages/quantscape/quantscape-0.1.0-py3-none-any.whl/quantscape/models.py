import numpy as np
from scipy.stats import norm
from scipy import integrate


class BlackScholes: 
    """
    A class to represent the Black-Scholes option pricing model.
    """   
    def __init__(self, K, r, S0, T, sigma): 
        """
        Initialize BlackScholes with strike price, risk-free rate, initial stock price,
        time to expiration, and volatility.
        
        Parameters:
        - K: float
            Strike price of the option.
        - r: float
            Risk-free interest rate.
        - S0: float
            Initial stock price.
        - T: float
            Time to expiration (in years).
        - sigma: float
            Volatility of the underlying stock.
        """
        self.K = K
        self.r = r
        self.S0 = S0
        self.T = T
        self.sigma = sigma
        
        self.d1 = (np.log(S0/self.K) + (self.r + ((self.sigma**2)/2))*self.T) / (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma*np.sqrt(self.T)
        
    def call(self):
        """
        Calculate the Black-Scholes call option price.
        
        Returns:
        - float
            Call option price.
        """
        return (self.S0 * norm.cdf(self.d1, 0, 1)) - (self.K * np.exp(-self.r*self.T) * norm.cdf(self.d2, 0, 1))
        
    def put(self):
        """
        Calculate the Black-Scholes put option price.
        
        Returns:
        - float
            Put option price.
        """
        return self.K * np.exp(self.r*self.T) * norm.cdf(-self.d2, 0 , 1) - self.S0 * norm.cdf(-self.d1, 0, 1)
    
    # Delta for call and put
    def delta(self, option_type="call"):
        """
        Calculate the Black-Scholes delta for the option.

        Parameters:
        - option_type: str (optional, default="call")
            Type of the option ("call" or "put").

        Returns:
        - float
            Delta of the option.
        """
        if option_type == "call":
            return norm.cdf(self.d1, 0, 1)
        elif option_type == "put":
            return norm.cdf(self.d1, 0, 1) - 1
    
    def gamma(self):
        """
        Calculate the Black-Scholes gamma for the option.
        
        Returns:
        - float
            Gamma of the option.
        """
        return norm.pdf(self.d1, 0, 1) / (self.S0 * self.sigma * np.sqrt(self.T))
    

    def theta(self, option_type="call"):
        """
        Calculate the Black-Scholes theta (time decay) for the option.

        Parameters:
        - option_type: str (optional, default="call")
            Type of the option ("call" or "put").

        Returns:
        - float
            Theta of the option.
        """
        if option_type == "call":
            theta = (-self.S0 * norm.pdf(self.d1, 0, 1) * self.sigma / (2 * np.sqrt(self.T))) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2, 0, 1)
        elif option_type == "put":
            theta = (-self.S0 * norm.pdf(self.d1, 0, 1) * self.sigma / (2 * np.sqrt(self.T))) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2, 0, 1)
        return theta / 365
    
    def vega(self):
        """
        Calculate the Black-Scholes vega for the option.
        
        Returns:
        - float
            Vega of the option.
        """
        return self.S0 * norm.pdf(self.d1, 0, 1) * np.sqrt(self.T) * 0.01
    

    def rho(self, option_type="call"):
        """
        Calculate the Black-Scholes rho (sensitivity to interest rate) for the option.

        Parameters:
        - option_type: str (optional, default="call")
            Type of the option ("call" or "put").

        Returns:
        - float
            Rho of the option.
        """
        if option_type == "call":
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2, 0, 1) * 0.01
        elif option_type == "put":
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2, 0, 1) * 0.01


class Heston:
    """
    A class to represent the Heston stochastic volatility model for option pricing.
    """
    def __init__(self, r, q, s, v, kappa, theta, sigma_v, rho, T):
        """
        Initialize Heston model with necessary parameters.
        
        Parameters:
        - r: float
            Risk-free interest rate.
        - q: float
            Dividend yield.
        - s: float
            Current stock price.
        - v: float
            Current variance.
        - kappa: float
            Rate at which v reverts to theta.
        - theta: float
            Long-term average price variance.
        - sigma_v: float
            Volatility of volatility.
        - rho: float
            Correlation between price returns and variance.
        - T: float
            Time to expiration (in years).
        """
        self.r = r
        self.q = q
        self.s = s
        self.v = v
        self.kappa = kappa
        self.theta = theta
        self.sigma_v = sigma_v
        self.rho = rho
        self.T = T

    def phi(self, u):
        """
        Helper function to compute the characteristic function for Heston model.

        Parameters:
        - u: float
            Input value for which the characteristic function is to be computed.

        Returns:
        - float
            Value of the characteristic function.
        """
        alpha_hat = -0.5 * u * (u + 1j)
        beta = self.kappa - 1j * u * self.sigma_v * self.rho
        gamma = 0.5 * self.sigma_v ** 2
        d = np.sqrt(beta**2 - 4 * alpha_hat * gamma)
        g = (beta - d) / (beta + d)
        h = np.exp(-d * self.T)
        A_ = (beta - d) * self.T - 2 * np.log((g * h - 1) / (g - 1))
        A = self.kappa * self.theta / (self.sigma_v**2) * A_
        B = (beta - d) / (self.sigma_v**2) * (1 - h) / (1 - g * h)
        return np.exp(A + B * self.v)

    def integral(self, k):
        """
        Compute the integral part of the Heston model formula.

        Parameters:
        - k: float
            Logarithm of the strike to stock price ratio.

        Returns:
        - float
            Integral value.
        """
        integrand = (lambda u: 
            np.real(np.exp((1j * u + 0.5) * k) * self.phi(u - 0.5j)) / (u**2 + 0.25))

        i, _ = integrate.quad(integrand, 0, np.inf)
        return i

    def call(self, strike):
        """
        Calculate the call option price using the Heston model.

        Parameters:
        - strike: float
            Strike price of the option.

        Returns:
        - float
            Call option price.
        """
        a = np.log(self.s / strike) + (self.r - self.q) * self.T
        i = self.integral(a)        
        call_price = self.s * np.exp(-self.q * self.T) - strike * np.exp(-self.r * self.T) / np.pi * i
        return call_price

    def put(self, strike):
        """
        Calculate the put option price using the Heston model.

        Parameters:
        - strike: float
            Strike price of the option.

        Returns:
        - float
            Put option price.
        """
        call_price = self.call(strike)
        put_price = call_price - self.s * np.exp(-self.q * self.T) + strike * np.exp(-self.r * self.T)
        return put_price
    

class ImpliedVolatility:
    """
    A class to represent the implied volatility calculations for options.
    """
    def __init__(self, K, r, S0, T, c, p):
        """
        Initialize ImpliedVolatility with necessary parameters.
        
        Parameters:
        - K: float
            Strike price of the option.
        - r: float
            Risk-free interest rate.
        - S0: float
            Initial stock price.
        - T: float
            Time to expiration (in years).
        - c: float
            Call option market price.
        - p: float
            Put option market price.
        """
        self.K = K
        self.r = r
        self.S0 = S0
        self.T = T
        self.c = c  
        self.p = p  

    def black_scholes(self, sigma, option_type):
        """
        Compute the Black-Scholes option price for a given volatility.

        Parameters:
        - sigma: float
            Volatility of the underlying stock.
        - option_type: str
            Type of the option ("call" or "put").

        Returns:
        - float
            Option price.
        """
        d1 = (np.log(self.S0/self.K) + (self.r + ((sigma**2)/2))*self.T) / (sigma * np.sqrt(self.T))
        d2 = d1 - sigma*np.sqrt(self.T)
        
        if option_type == 'call':
            return (self.S0 * norm.cdf(d1, 0, 1)) - (self.K * np.exp(-self.r*self.T) * norm.cdf(d2, 0, 1))
        if option_type == 'put':
            return (self.K * np.exp(self.r*self.T) * norm.cdf(-d2, 0 , 1) - self.S0 * norm.cdf(-d1, 0, 1))

    def bisection_search(self, option_type):
        """
        Use bisection search to estimate implied volatility.

        Parameters:
        - option_type: str
            Type of the option ("call" or "put").

        Returns:
        - float
            Implied volatility.
        """
        tolerance = 0.001 
        max_attempts = 1000 

        lower_bound = 0
        upper_bound = 1
        sigma_guess = (lower_bound + upper_bound)/2
        
        if option_type == 'call':
            real_option_price = self.c
            guess_price = self.black_scholes(sigma_guess, 'call')
        elif option_type == 'put':
            real_option_price = self.p
            guess_price = self.black_scholes(sigma_guess, 'put')
        
        print(f'Guess price: {guess_price}, sigma: {sigma_guess}')
        
        error = (abs(real_option_price - guess_price))
        print(f'Error: {error}')
        attempts = 0

        while error > tolerance and attempts < max_attempts: 
            if guess_price > real_option_price:
                upper_bound = sigma_guess
            elif guess_price < real_option_price:
                lower_bound = sigma_guess

            sigma_guess = (lower_bound + upper_bound)/2
            
            if option_type == 'call':
                guess_price = self.black_scholes(sigma_guess, 'call')
            elif option_type == 'put':
                guess_price = self.black_scholes(sigma_guess, 'put')
                
            print(f'new guess price {guess_price}, new sigma: {sigma_guess}')

            error = abs(real_option_price - guess_price)
            attempts += 1

        return sigma_guess
    
    def calculate_sigma(self, option_type):
        """
        Calculate implied volatility for a given option type.

        Parameters:
        - option_type: str
            Type of the option ("call" or "put").

        Returns:
        - float
            Implied volatility.
        """
        if option_type == 'call':
            return self.bisection_search('call')
        elif option_type == 'put':
            return self.bisection_search('put')
