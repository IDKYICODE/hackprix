import { Tabs } from "expo-router";
import { Ionicons } from '@expo/vector-icons';
import { Text } from 'react-native';

export default function TabsLayout() {
  return (
    <Tabs 
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: '#00c6ff',
        tabBarIcon: ({ color, size, focused }) => {
          let iconName: React.ComponentProps<typeof Ionicons>['name'] = 'alert-circle-outline';

          // Use the lowercase name for icon logic, but the route name itself is capitalized
          const routeName = route.name.toLowerCase();

          if (routeName === 'home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (routeName === 'marketplace') {
            iconName = focused ? 'cart' : 'cart-outline';
          } else if (routeName === 'lounge') {
            iconName = focused ? 'game-controller' : 'game-controller-outline';
          } else if (routeName === 'profile') {
            iconName = focused ? 'person' : 'person-outline';
          }

          try {
            return <Ionicons name={iconName} size={size} color={color} />;
          } catch (error) {
            // Fallback if icons fail to load
            return <Text>!</Text>;
          }
        },
      })}
    >
      {/* Correct the screen name to match the file name "Home.tsx" */}
      <Tabs.Screen name="Home" options={{ title: "Home" }} />
      <Tabs.Screen name="marketplace" options={{ title: "Marketplace" }} />
      <Tabs.Screen name="lounge" options={{ title: "Lounge" }} />
      <Tabs.Screen name="profile" options={{ title: "Profile" }} />
    </Tabs>
  );
}
