import { Zap, Coins, Flame } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useNavigate } from "react-router-dom";

const subjects = [
  {
    id: "math",
    name: "Mathematics",
    icon: "🔢",
    color: "from-blue-500 to-cyan-500",
    progress: 65,
  },
  {
    id: "physics",
    name: "Physics",
    icon: "⚛️",
    color: "from-purple-500 to-pink-500",
    progress: 42,
  },
  {
    id: "chemistry",
    name: "Chemistry",
    icon: "🧪",
    color: "from-green-500 to-emerald-500",
    progress: 78,
  },
  {
    id: "biology",
    name: "Biology",
    icon: "🧬",
    color: "from-orange-500 to-red-500",
    progress: 55,
  },
];

const Home = () => {
  const navigate = useNavigate();
  const userXP = 2450;
  const userCoins = 850;
  const streak = 7;

  return (
    <div className="pb-20 px-4 pt-6 max-w-lg mx-auto min-h-screen">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gradient mb-2">EduVerse</h1>
        <p className="text-muted-foreground">Your Immersive Learning Journey</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-3 gap-3 mb-6">
        <Card className="p-4 shadow-card gradient-card border-accent/20">
          <div className="flex items-center gap-2 mb-2">
            <Flame className="w-5 h-5 text-orange-500" />
            <span className="text-xs text-muted-foreground">Streak</span>
          </div>
          <p className="text-2xl font-bold">{streak}</p>
          <p className="text-xs text-muted-foreground">days</p>
        </Card>

        <Card className="p-4 shadow-card gradient-card border-accent/20">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-accent" />
            <span className="text-xs text-muted-foreground">XP</span>
          </div>
          <p className="text-2xl font-bold">{userXP}</p>
          <p className="text-xs text-muted-foreground">points</p>
        </Card>

        <Card className="p-4 shadow-card gradient-card border-secondary/20">
          <div className="flex items-center gap-2 mb-2">
            <Coins className="w-5 h-5 text-secondary" />
            <span className="text-xs text-muted-foreground">Coins</span>
          </div>
          <p className="text-2xl font-bold">{userCoins}</p>
          <p className="text-xs text-muted-foreground">tokens</p>
        </Card>
      </div>

      {/* Daily Quest */}
      <Card className="p-4 mb-6 shadow-card border-accent/30 gradient-card">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-foreground">Daily Quest</h3>
          <span className="text-xs bg-accent/20 text-accent px-2 py-1 rounded-full font-medium">
            +100 XP
          </span>
        </div>
        <p className="text-sm text-muted-foreground mb-3">
          Watch 1 lesson + Play 1 VR Game
        </p>
        <Progress value={50} className="h-2" />
        <p className="text-xs text-muted-foreground mt-2">1/2 completed</p>
      </Card>

      {/* Subjects Section */}
      <div className="mb-6">
        <h2 className="text-xl font-bold mb-4">Your Subjects</h2>
        <div className="grid grid-cols-2 gap-4">
          {subjects.map((subject) => (
            <Card
              key={subject.id}
              className="p-5 cursor-pointer transition-all hover:scale-105 hover:shadow-float shadow-card gradient-card border-border"
              onClick={() => navigate(`/subject/${subject.id}`)}
            >
              <div
                className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${subject.color} flex items-center justify-center text-3xl mb-3 shadow-lg`}
              >
                {subject.icon}
              </div>
              <h3 className="font-semibold mb-2 text-foreground">{subject.name}</h3>
              <div className="space-y-2">
                <Progress value={subject.progress} className="h-1.5" />
                <p className="text-xs text-muted-foreground">{subject.progress}% Complete</p>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <Card className="p-4 shadow-card gradient-cyber">
        <h3 className="font-semibold text-primary-foreground mb-3">Quick Actions</h3>
        <div className="grid grid-cols-2 gap-3">
          <button className="bg-white/10 hover:bg-white/20 backdrop-blur text-primary-foreground rounded-xl p-3 text-sm font-medium transition-all">
            📚 Continue Learning
          </button>
          <button className="bg-white/10 hover:bg-white/20 backdrop-blur text-primary-foreground rounded-xl p-3 text-sm font-medium transition-all">
            🎮 Join VR Game
          </button>
        </div>
      </Card>
    </div>
  );
};

export default Home;