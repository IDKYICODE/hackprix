import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Coins, ShoppingCart } from "lucide-react";
import { toast } from "sonner";

const items = [
  {
    id: 1,
    name: "Physics Textbook",
    category: "Books",
    price: 250,
    icon: "📚",
    description: "Complete guide to quantum mechanics",
  },
  {
    id: 2,
    name: "VR Headset Skin",
    category: "VR Gear",
    price: 500,
    icon: "🥽",
    description: "Holographic blue theme",
  },
  {
    id: 3,
    name: "Lab Coat Avatar",
    category: "Avatars",
    price: 350,
    icon: "🥼",
    description: "Professional scientist outfit",
  },
  {
    id: 4,
    name: "Chemistry Set",
    category: "Items",
    price: 400,
    icon: "⚗️",
    description: "Virtual experiment kit",
  },
  {
    id: 5,
    name: "Math Genius Badge",
    category: "Badges",
    price: 300,
    icon: "🏆",
    description: "Show off your skills",
  },
  {
    id: 6,
    name: "Neon Particle Effect",
    category: "Effects",
    price: 450,
    icon: "✨",
    description: "Animated trail effect",
  },
];

const Marketplace = () => {
  const userCoins = 850;

  const handlePurchase = (item: typeof items[0]) => {
    if (userCoins >= item.price) {
      toast.success(`Purchased ${item.name}! 🎉`);
    } else {
      toast.error("Not enough EduCoins! 💰");
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
              <p className="text-2xl font-bold text-white">{userCoins}</p>
            </div>
          </div>
          <ShoppingCart className="w-6 h-6 text-white/80" />
        </div>
      </Card>

      {/* Items Grid */}
      <div className="space-y-3">
        {items.map((item) => (
          <Card
            key={item.id}
            className="p-4 shadow-card gradient-card border-border hover:border-accent/50 transition-all"
          >
            <div className="flex gap-4">
              <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-accent/20 to-secondary/20 flex items-center justify-center text-3xl flex-shrink-0">
                {item.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2 mb-1">
                  <h3 className="font-semibold text-foreground">{item.name}</h3>
                  <div className="flex items-center gap-1 bg-secondary/10 px-2 py-1 rounded-full flex-shrink-0">
                    <Coins className="w-4 h-4 text-secondary" />
                    <span className="text-sm font-bold text-secondary">{item.price}</span>
                  </div>
                </div>
                <p className="text-xs text-accent mb-1">{item.category}</p>
                <p className="text-sm text-muted-foreground mb-3">{item.description}</p>
                <Button
                  size="sm"
                  className="w-full bg-accent hover:bg-accent/90 text-accent-foreground glow-cyan"
                  onClick={() => handlePurchase(item)}
                >
                  Purchase
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Marketplace;
