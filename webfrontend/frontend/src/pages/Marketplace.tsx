import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Coins, ShoppingCart, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "@/context/AuthContext";
import { fetchProducts, addToCart } from "@/lib/authClient";
import { Product } from "@/types";

const Marketplace = () => {
  const { user } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        setLoading(true);
        const data = await fetchProducts();
        setProducts(data);
      } catch (error) {
        toast.error("Failed to fetch products.");
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  const handleAddToCart = async (productId: number) => {
    try {
      await addToCart(productId, 1);
      toast.success("Item added to cart! 🛒");
    } catch (error) {
      toast.error("Failed to add item to cart.");
    }
  };

  return (
    <div className="pb-20 px-4 pt-6 max-w-lg mx-auto min-h-screen">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gradient mb-2">Marketplace</h1>
        <p className="text-muted-foreground">Spend your EduCoins wisely</p>
      </div>

      {/* Wallet */}
      <Card className="p-4 mb-6 shadow-card gradient-neon">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur flex items-center justify-center">
              <Coins className="w-6 h-6 text-white" />
            </div>
            <div>
              <p className="text-sm text-white/80">Your Balance</p>
              <p className="text-2xl font-bold text-white">{user?.edu_coins ?? 0}</p>
            </div>
          </div>
          <ShoppingCart className="w-6 h-6 text-white/80" />
        </div>
      </Card>

      {/* Items Grid */}
      {loading ? (
        <div className="flex justify-center mt-20">
          <Loader2 className="w-10 h-10 text-primary animate-spin" />
        </div>
      ) : (
        <div className="space-y-3">
          {products.map((item) => (
            <Card
              key={item.id}
              className="p-4 shadow-card gradient-card border-border hover:border-accent/50 transition-all"
            >
              <div className="flex gap-4">
                <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-accent/20 to-secondary/20 flex items-center justify-center text-3xl flex-shrink-0">
                  {/* Displaying a placeholder if no thumbnail */}
                  {item.thumbnail ? <img src={item.thumbnail} alt={item.name} className="w-full h-full object-cover rounded-xl" /> : '🛍️'}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <h3 className="font-semibold text-foreground">{item.name}</h3>
                    <div className="flex items-center gap-1 bg-secondary/10 px-2 py-1 rounded-full flex-shrink-0">
                      <Coins className="w-4 h-4 text-secondary" />
                      <span className="text-sm font-bold text-secondary">{item.points_price}</span>
                    </div>
                  </div>
                  <p className="text-xs text-accent mb-1">{item.category_name}</p>
                  <p className="text-sm text-muted-foreground mb-3">{item.description}</p>
                  <Button
                    size="sm"
                    className="w-full bg-accent hover:bg-accent/90 text-accent-foreground glow-cyan"
                    onClick={() => handleAddToCart(item.id)}
                  >
                    Add to Cart
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Marketplace;
