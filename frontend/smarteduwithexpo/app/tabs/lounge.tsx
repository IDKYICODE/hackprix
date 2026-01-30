import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image, Linking } from "react-native";
import { LinearGradient } from 'expo-linear-gradient';

export default function Lounge() {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.headerTitle}>VR Lounge</Text>
      <Text style={styles.headerSubtitle}>Jump into immersive learning games</Text>

      <LinearGradient
        colors={['#6a11cb', '#2575fc']}
        style={styles.lobbyCard}
      >
        <Text style={styles.lobbyTitle}>Virtual Campus Lobby</Text>
        <Text style={styles.lobbySubtitle}>Choose a portal to enter a subject's VR game world</Text>
      </LinearGradient>

      <View style={styles.gameCard}>
        <Image source={{ uri: 'https://cdn-icons-png.flaticon.com/512/2990/2990134.png' }} style={styles.gameImage} />
        <View style={styles.gameDetails}>
          <Text style={styles.gameName}>Cell City Siege</Text>
          <Text style={styles.gameCategory}>Biology</Text>
          <Text style={styles.gameDescription}>Battle viruses inside a 3D cell</Text>
        </View>
        <View style={styles.joinContainer}>
            <Text style={styles.playerCount}>12/20</Text>
            <TouchableOpacity 
              style={styles.joinButton}
              onPress={() => Linking.openURL('https://blood-game-c44cb.web.app/')}
            >
                <Text style={styles.joinButtonText}>Join Room</Text>
            </TouchableOpacity>
        </View>
      </View>

      <View style={styles.gameCard}>
        <Image source={{ uri: 'https://cdn-icons-png.flaticon.com/512/330/330351.png' }} style={styles.gameImage} />
        <View style={styles.gameDetails}>
          <Text style={styles.gameName}>Molecule Builder</Text>
          <Text style={styles.gameCategory}>Chemistry</Text>
          <Text style={styles.gameDescription}>Build 3D molecules in VR</Text>
        </View>
        <View style={styles.joinContainer}>
            <Text style={styles.playerCount}>8/15</Text>
            <TouchableOpacity 
              style={styles.joinButton}
              onPress={() => Linking.openURL('https://molecule-builder-911c7.web.app/')}
            >
                <Text style={styles.joinButtonText}>Join Room</Text>
            </TouchableOpacity>
        </View>
      </View>

      <View style={styles.gameCard}>
        <Image source={{ uri: 'https://cdn-icons-png.flaticon.com/512/1049/1049593.png' }} style={styles.gameImage} />
        <View style={styles.gameDetails}>
          <Text style={styles.gameName}>Anatomy VR Labroom</Text>
          <Text style={styles.gameCategory}>Biology</Text>
          <Text style={styles.gameDescription}>Explore 3D anatomy models in a virtual lab</Text>
        </View>
        <View style={styles.joinContainer}>
            <Text style={styles.playerCount}>10/20</Text>
            <TouchableOpacity 
              style={styles.joinButton}
              onPress={() => Linking.openURL('https://my-anatomy-vr-2026.web.app/')}
            >
                <Text style={styles.joinButtonText}>Join Room</Text>
            </TouchableOpacity>
        </View>
      </View>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f0f2f5',
        padding: 20,
    },
    headerTitle: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#007bff',
    },
    headerSubtitle: {
        fontSize: 16,
        color: '#6c757d',
        marginBottom: 20,
    },
    lobbyCard: {
        borderRadius: 15,
        padding: 25,
        marginBottom: 20,
        alignItems: 'center'
    },
    lobbyTitle: {
        color: '#fff',
        fontSize: 22,
        fontWeight: 'bold',
    },
    lobbySubtitle: {
        color: '#fff',
        fontSize: 14,
        textAlign: 'center',
        marginTop: 5
    },
    gameCard: {
        backgroundColor: '#fff',
        borderRadius: 10,
        padding: 15,
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 15,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.22,
        shadowRadius: 2.22,
        elevation: 3,
    },
    gameImage: {
        width: 60,
        height: 60,
        marginRight: 15,
    },
    gameDetails: {
        flex: 1,
    },
    gameName: {
        fontSize: 18,
        fontWeight: 'bold',
    },
    gameCategory: {
        fontSize: 14,
        color: '#6c757d',
    },
    gameDescription: {
        fontSize: 12,
        color: '#6c757d',
        marginTop: 5,
    },
    playerCount: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#28a745',
        marginBottom: 5
    },
    joinButton: {
        backgroundColor: '#00c6ff',
        borderRadius: 20,
        paddingVertical: 5,
        paddingHorizontal: 15,
    },
    joinButtonText: {
        color: '#fff',
        fontWeight: 'bold',
        textAlign: 'center'
    },
    joinContainer: {
        alignItems: 'center'
    }
});
