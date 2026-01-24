import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Award, Trophy, Star, Settings } from "lucide-react";

const badges = [
  { id: 1, name: "Math Master", icon: "🔢", earned: true },
  { id: 2, name: "Chemistry Pro", icon: "🧪", earned: true },
  { id: 3, name: "VR Champion", icon: "🥽", earned: true },
  { id: 4, name: "7-Day Streak", icon: "🔥", earned: true },
  { id: 5, name: "Physics Wizard", icon: "⚛️", earned: false },
  { id: 6, name: "Biology Expert", icon: "🧬", earned: false },
];

const achievements = [
  { title: "Completed 10 Lessons", date: "2 days ago", xp: 100 },
  { title: "Won VR Game", date: "3 days ago", xp: 50 },
  { title: "Purchased First Item", date: "5 days ago", xp: 25 },
];

const Profile = () => {
  const userName = "Alex Chen";
  const userLevel = 12;
  const userXP = 2450;
  const nextLevelXP = 3000;
  const userCoins = 850;
  const xpProgress = (userXP / nextLevelXP) * 100;

  return (
    <div className="pb-20 px-4 pt-6 max-w-lg mx-auto min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Profile</h1>
          <p className="text-muted-foreground">Track your learning journey</p>
        </div>
        <Button size="icon" variant="outline" className="rounded-xl">
          <Settings className="w-5 h-5" />
        </Button>
      </div>

      {/* Profile Card */}
      <Card className="p-6 mb-6 shadow-float gradient-cyber">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-accent to-secondary flex items-center justify-center text-4xl shadow-lg">
            👨‍🚀
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-primary-foreground">{userName}</h2>
            <div className="flex items-center gap-2 mt-1">
              <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
              <span className="text-primary-foreground font-semibold">Level {userLevel}</span>
            </div>
          </div>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-primary-foreground/80">
            <span>XP Progress</span>
            <span>
              {userXP} / {nextLevelXP}
            </span>
          </div>
          <Progress value={xpProgress} className="h-2" />
        </div>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <Card className="p-4 shadow-card gradient-card border-accent/20">
          <Trophy className="w-8 h-8 text-accent mb-2" />
          <p className="text-2xl font-bold">{userXP}</p>
          <p className="text-sm text-muted-foreground">Total XP</p>
        </Card>
        <Card className="p-4 shadow-card gradient-card border-secondary/20">
          <Award className="w-8 h-8 text-secondary mb-2" />
          <p className="text-2xl font-bold">{userCoins}</p>
          <p className="text-sm text-muted-foreground">EduCoins</p>
        </Card>
      </div>

      {/* Badges Section */}
      <div className="mb-6">
        <h3 className="text-lg font-bold mb-3">Your Badges</h3>
        <Card className="p-4 shadow-card gradient-card">
          <div className="grid grid-cols-3 gap-3">
            {badges.map((badge) => (
              <div
                key={badge.id}
                className={`p-3 rounded-xl text-center transition-all ${
                  badge.earned
                    ? "bg-gradient-to-br from-accent/20 to-secondary/20 border border-accent/30"
                    : "bg-muted/30 opacity-50"
                }`}
              >
                <div className="text-3xl mb-1">{badge.icon}</div>
                <p className="text-xs font-medium">{badge.name}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Recent Achievements */}
      <div className="mb-6">
        <h3 className="text-lg font-bold mb-3">Recent Achievements</h3>
        <div className="space-y-3">
          {achievements.map((achievement, idx) => (
            <Card key={idx} className="p-4 shadow-card gradient-card border-border">
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-semibold text-foreground">{achievement.title}</p>
                  <p className="text-sm text-muted-foreground">{achievement.date}</p>
                </div>
                <span className="text-sm font-bold text-accent">+{achievement.xp} XP</span>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-3">
        <Button variant="outline" className="w-full">
          📜 My Certificates
        </Button>
        <Button variant="outline" className="w-full">
          ✏️ Edit Avatar
        </Button>
      </div>
    </div>
  );
};

export default Profile;
