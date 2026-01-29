// src/types.ts
export interface User {
    id: number;
    username: string;
    email: string;
    role: "student" | "teacher" | "admin";
    institution: number | null;
    institution_name: string | null;
    class_group: number | null;
    class_group_name: string | null;
    wallet_address: string | null;
    mobile_number: string | null;
    profile_image: string | null;
    gender: "male" | "female" | "other" | null;
    date_of_birth: string | null;
    bio: string | null;
  }
  
export interface ProductCategory {
    id: number;
    name: string;
    slug: string;
    description: string;
    is_active: boolean;
  }
  
export interface Product {
    id: number;
    category: number;
    category_name: string;
    name: string;
    description: string;
    product_type: string;
    points_price: number;
    stock: number | null;
    is_digital: boolean;
    digital_file: string | null;
    external_url: string | null;
    thumbnail: string | null;
    metadata: any | null;
    is_active: boolean;
    featured: boolean;
    created_at: string;
    updated_at: string;
    is_unlimited: boolean;
  }
  
export interface CartItem {
    id: number;
    product: Product;
    quantity: number;
    total_points: number;
  }
  
export interface Cart {
    id: number;
    user: number;
    items: CartItem[];
    total_cart_points: number;
    created_at: string;
  }
  
export interface Redemption {
    id: number;
    user: number;
    user_username: string;
    product: number;
    product_name: string;
    quantity: number;
    points_spent: number;
    status: string;
    tx_hash: string | null;
    delivery_email: string | null;
    delivery_notes: string | null;
    shipping_address: string | null;
    contact_phone: string | null;
    created_at: string;
    updated_at: string;
  }