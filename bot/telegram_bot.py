"""
E-commerce Telegram Bot
Integrated with Backend API for Order Management
Business Process: E-commerce Order Management System
"""

import os
import json
import asyncio
import logging
from typing import Optional
import aiohttp
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# ===== CONFIGURATION =====

# Telegram Bot Token - Replace with your actual token from BotFather
BOT_TOKEN = "8575314734:AAEIOZXWs40Ho3QkhxIYZhowbB5e5unOTjE"

# Backend API Configuration
BACKEND_URL = "http://localhost:3000/api"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== CONVERSATION STATES =====
MAIN_MENU, BROWSE_PRODUCTS, SELECT_PRODUCT, ADD_TO_CART, VIEW_CART, CHECKOUT, CUSTOMER_NAME, CUSTOMER_EMAIL, CUSTOMER_PHONE, DELIVERY_ADDRESS = range(10)

# ===== API CLIENT =====

class BackendAPIClient:
    """Client for communicating with the backend API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    async def register_user(self, telegram_id: int, username: str, first_name: str):
        """Register or get user from backend"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/users/register",
                    json={
                        "telegram_id": str(telegram_id),
                        "username": username or "bot_user",
                        "first_name": first_name or "User"
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Error registering user: {resp.status}")
                        return None
            except Exception as e:
                logger.error(f"API Error in register_user: {e}")
                return None
    
    async def get_products(self):
        """Fetch all products from backend"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/products",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Error fetching products: {resp.status}")
                        return None
            except Exception as e:
                logger.error(f"API Error in get_products: {e}")
                return None
    
    async def add_to_cart(self, telegram_id: int, product_id: str, quantity: int):
        """Add item to user's cart"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/cart/add",
                    json={
                        "telegram_id": str(telegram_id),
                        "product_id": product_id,
                        "quantity": quantity
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        data = await resp.text()
                        logger.error(f"Error adding to cart: {data}")
                        return None
            except Exception as e:
                logger.error(f"API Error in add_to_cart: {e}")
                return None
    
    async def get_cart(self, telegram_id: int):
        """Get user's cart"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/cart/{telegram_id}",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Error fetching cart: {resp.status}")
                        return None
            except Exception as e:
                logger.error(f"API Error in get_cart: {e}")
                return None
    
    async def remove_from_cart(self, telegram_id: int, product_id: str):
        """Remove item from cart"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/cart/remove",
                    json={
                        "telegram_id": str(telegram_id),
                        "product_id": product_id
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Error removing from cart: {resp.status}")
                        return None
            except Exception as e:
                logger.error(f"API Error in remove_from_cart: {e}")
                return None
    
    async def create_order(self, telegram_id: int, delivery_address: str, payment_method: str = "CARD"):
        """Create order from cart"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/orders/create",
                    json={
                        "telegram_id": str(telegram_id),
                        "delivery_address": delivery_address,
                        "payment_method": payment_method
                    },
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        data = await resp.text()
                        logger.error(f"Error creating order: {data}")
                        return None
            except Exception as e:
                logger.error(f"API Error in create_order: {e}")
                return None
    
    async def get_user_orders(self, telegram_id: int):
        """Get all orders for a user"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"{self.base_url}/orders/user/{telegram_id}",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Error fetching orders: {resp.status}")
                        return None
            except Exception as e:
                logger.error(f"API Error in get_user_orders: {e}")
                return None

# Initialize API Client
api_client = BackendAPIClient(BACKEND_URL)

# ===== BOT COMMAND HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - Register user and show main menu"""
    user = update.effective_user
    
    # Register user with backend
    registration = await api_client.register_user(
        user.id,
        user.username or "unknown",
        user.first_name or "User"
    )
    
    if registration:
        welcome_text = f"🎉 Welcome to *EduMart Store*, {user.first_name}!\n\n"
        welcome_text += "Your online shopping assistant for tech products.\n\n"
        welcome_text += "What would you like to do?"
        
        await show_main_menu(update, context)
    else:
        await update.message.reply_text(
            "❌ Sorry, I couldn't connect to the backend. Please try again later."
        )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display main menu with inline keyboard"""
    keyboard = [
        [InlineKeyboardButton("🛍️ Browse Products", callback_data="browse_products")],
        [InlineKeyboardButton("🛒 View Cart", callback_data="view_cart")],
        [InlineKeyboardButton("📦 My Orders", callback_data="my_orders")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="*Main Menu* 🏠\n\nSelect an option:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "*Main Menu* 🏠\n\nSelect an option:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
*🛍️ EduMart Store - Help*

*Available Commands:*
/start - Start the bot and show main menu
/help - Show this help message
/products - Browse all products
/cart - View your shopping cart
/orders - View your order history

*How to Use:*
1. Browse Products - View available items
2. Add to Cart - Select products and add quantities
3. View Cart - Review items before checkout
4. Checkout - Enter delivery address and create order
5. Track Orders - Monitor your order status

*Support:*
For issues, please contact our support team.
    """
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show products"""
    await show_products(update, context)

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch and display products"""
    products_data = await api_client.get_products()
    
    if not products_data or not products_data.get('products'):
        if update.callback_query:
            await update.callback_query.answer("❌ Could not fetch products", show_alert=True)
        else:
            await update.message.reply_text("❌ Could not fetch products from server")
        return
    
    products = products_data['products']
    products_text = "*🛍️ Available Products:*\n\n"
    
    keyboard = []
    for product in products:
        products_text += f"• *{product['name']}* - ${product['price']}\n"
        products_text += f"  📦 Stock: {product['stock']} items\n\n"
        
        keyboard.append([InlineKeyboardButton(
            f"📌 {product['name']} - ${product['price']}",
            callback_data=f"select_product_{product['id']}"
        )])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=products_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            products_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display user's cart"""
    user_id = update.effective_user.id
    cart_data = await api_client.get_cart(user_id)
    
    if not cart_data:
        await update.callback_query.answer("❌ Could not fetch cart", show_alert=True)
        return
    
    cart = cart_data.get('cart', [])
    total = cart_data.get('total', '0.00')
    
    if not cart:
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text="🛒 *Your Cart is Empty*\n\nStart shopping by browsing products!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    cart_text = "*🛒 Your Shopping Cart:*\n\n"
    keyboard = []
    
    for item in cart:
        item_total = float(item['price']) * item['quantity']
        cart_text += f"• *{item['name']}*\n"
        cart_text += f"  Price: ${item['price']} × {item['quantity']} = ${item_total:.2f}\n\n"
        
        keyboard.append([
            InlineKeyboardButton(
                f"❌ Remove {item['name']}",
                callback_data=f"remove_from_cart_{item['product_id']}"
            )
        ])
    
    cart_text += f"\n*Total: ${total}*"
    
    keyboard.append([InlineKeyboardButton("💳 Proceed to Checkout", callback_data="checkout")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        text=cart_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display user's orders"""
    user_id = update.effective_user.id
    orders_data = await api_client.get_user_orders(user_id)
    
    if not orders_data or not orders_data.get('orders'):
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(
            text="📦 *Your Orders*\n\nYou haven't placed any orders yet!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    orders = orders_data['orders']
    orders_text = "*📦 Your Orders:*\n\n"
    
    for order in orders:
        status_emoji = {
            'PENDING': '⏳',
            'CONFIRMED': '✅',
            'PROCESSING': '⚙️',
            'SHIPPED': '🚚',
            'DELIVERED': '📦',
            'CANCELLED': '❌'
        }.get(order['status'], '❓')
        
        orders_text += f"{status_emoji} *Order {order['order_id'][:8]}...*\n"
        orders_text += f"  Total: ${order['total']}\n"
        orders_text += f"  Status: {order['status']}\n"
        orders_text += f"  Date: {order['created_at'][:10]}\n\n"
    
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        text=orders_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about information"""
    about_text = """
*ℹ️ About EduMart Store*

An innovative e-commerce platform designed for seamless shopping experience.

*Features:*
✅ Browse wide range of tech products
✅ Add items to cart
✅ Secure checkout process
✅ Order tracking
✅ Real-time inventory management

*Technology Stack:*
• Backend: Node.js + Express
• Bot: Python + python-telegram-bot
• Database: In-memory storage
• API: RESTful architecture

*Version:* 1.0.0
*Last Updated:* 2025

Enjoy shopping! 🛍️
    """
    
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        text=about_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Main menu navigation
    if data == "back_to_menu":
        await show_main_menu(update, context)
    
    elif data == "browse_products":
        await show_products(update, context)
    
    elif data == "view_cart":
        await show_cart(update, context)
    
    elif data == "my_orders":
        await show_orders(update, context)
    
    elif data == "about":
        await show_about(update, context)
    
    # Product selection
    elif data.startswith("select_product_"):
        product_id = data.replace("select_product_", "")
        await ask_quantity(update, context, product_id)
    
    # Remove from cart
    elif data.startswith("remove_from_cart_"):
        product_id = data.replace("remove_from_cart_", "")
        user_id = update.effective_user.id
        
        result = await api_client.remove_from_cart(user_id, product_id)
        if result and result.get('success'):
            await show_cart(update, context)
        else:
            await query.answer("❌ Could not remove item", show_alert=True)
    
    # Checkout
    elif data == "checkout":
        await query.answer()
        context.user_data['awaiting_customer_details'] = True
        context.user_data['customer_details'] = {}
        await update.effective_message.reply_text(
            "👤 *Customer Details*\n\n*Please enter your full name:*",
            parse_mode="Markdown"
        )

async def ask_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: str):
    """Ask user for quantity with product photo"""
    context.user_data['selected_product'] = product_id
    
    # Get product details to show name and photo
    products_data = await api_client.get_products()
    product_name = "Product"
    product_price = "N/A"
    product_image = None
    
    if products_data:
        for p in products_data.get('products', []):
            if p['id'] == product_id:
                product_name = p['name']
                product_price = p.get('price', 'N/A')
                product_image = p.get('image')
                break
    
    keyboard = [
        [InlineKeyboardButton("1", callback_data=f"qty_1_{product_id}"),
         InlineKeyboardButton("2", callback_data=f"qty_2_{product_id}"),
         InlineKeyboardButton("3", callback_data=f"qty_3_{product_id}"),
         InlineKeyboardButton("5", callback_data=f"qty_5_{product_id}")],
        [InlineKeyboardButton("10", callback_data=f"qty_10_{product_id}"),
         InlineKeyboardButton("⬅️ Back", callback_data="browse_products")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption = f"*{product_name}*\n💰 Price: ${product_price}\n\n*How many items would you like?*"
    
    try:
        # Try to send with photo if available
        if product_image:
            # Convert relative path to absolute path
            image_path = os.path.join(os.path.dirname(__file__), '..', product_image.lstrip('./'))
            
            if os.path.exists(image_path):
                # Use local file
                with open(image_path, 'rb') as photo:
                    await update.callback_query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption=caption, parse_mode="Markdown"),
                        reply_markup=reply_markup
                    )
            else:
                # Fallback to text if image doesn't exist
                logger.warning(f"Image not found: {image_path}, falling back to text")
                await update.callback_query.edit_message_text(
                    text=caption,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
        else:
            # Fallback to text if no image
            await update.callback_query.edit_message_text(
                text=caption,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
    except Exception as e:
        # If photo fails, fall back to text
        logger.warning(f"Could not send photo: {str(e)}, falling back to text")
        await update.callback_query.edit_message_text(
            text=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def handle_quantity_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quantity selection and add to cart"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("qty_"):
        parts = data.replace("qty_", "").split("_")
        quantity = int(parts[0])
        product_id = "_".join(parts[1:])
        
        user_id = update.effective_user.id
        result = await api_client.add_to_cart(user_id, product_id, quantity)
        
        if result and result.get('success'):
            keyboard = [
                [InlineKeyboardButton("🛒 View Cart", callback_data="view_cart")],
                [InlineKeyboardButton("🛍️ Continue Shopping", callback_data="browse_products")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"✅ *Added {quantity} item(s) to cart!*",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            await query.answer("❌ Could not add to cart", show_alert=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages - for customer details collection"""
    if context.user_data.get('awaiting_customer_details'):
        customer_details = context.user_data.get('customer_details', {})
        message_text = update.message.text.strip()
        
        # Collecting name
        if 'name' not in customer_details:
            customer_details['name'] = message_text
            context.user_data['customer_details'] = customer_details
            await update.message.reply_text(
                "📧 *Please enter your email address:*",
                parse_mode="Markdown"
            )
        # Collecting email
        elif 'email' not in customer_details:
            customer_details['email'] = message_text
            context.user_data['customer_details'] = customer_details
            await update.message.reply_text(
                "📱 *Please enter your phone number:*",
                parse_mode="Markdown"
            )
        # Collecting phone
        elif 'phone' not in customer_details:
            customer_details['phone'] = message_text
            context.user_data['customer_details'] = customer_details
            await update.message.reply_text(
                "📍 *Please enter your delivery address:*",
                parse_mode="Markdown"
            )
        # Collecting address
        elif 'address' not in customer_details:
            customer_details['address'] = message_text
            context.user_data['customer_details'] = customer_details
            context.user_data['awaiting_customer_details'] = False
            await receive_delivery_address(update, context)
    else:
        await update.message.reply_text(
            "ℹ️ Use the buttons below to navigate, or send /start to begin",
            parse_mode="Markdown"
        )

async def receive_delivery_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and process delivery address with customer details"""
    user_id = update.effective_user.id
    customer_details = context.user_data.get('customer_details', {})
    
    # Create order
    result = await api_client.create_order(user_id, customer_details.get('address', ''), "CARD")
    
    if result and result.get('success'):
        order = result['order']
        confirmation_text = f"""
*✅ Order Confirmed!*

*Customer Details:*
• Name: {customer_details.get('name', 'N/A')}
• Email: {customer_details.get('email', 'N/A')}
• Phone: {customer_details.get('phone', 'N/A')}

*Order Information:*
• Order ID: `{order['order_id']}`
• Total: ${order['total']}
• Status: {order['status']}
• Delivery Address: {customer_details.get('address', 'N/A')}

Your order has been placed successfully!
We'll update you on the status soon. 📦
        """
        
        keyboard = [
            [InlineKeyboardButton("📦 Track Orders", callback_data="my_orders")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(confirmation_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❌ Could not create order. Please try again.",
            parse_mode="Markdown"
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# ===== BOT SETUP AND MAIN =====

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[],
        states={
            DELIVERY_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_delivery_address)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    # Add handlers (order matters - more specific patterns first)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("products", products_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_quantity_selection, pattern=r"^qty_"))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("🤖 Telegram Bot is starting...")
    print(f"Backend URL: {BACKEND_URL}")
    application.run_polling()

if __name__ == '__main__':
    main()
