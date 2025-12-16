import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image } from "react-native";
import { LinearGradient } from 'expo-linear-gradient';

export default function Marketplace() {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.headerTitle}>Marketplace</Text>
      <Text style={styles.headerSubtitle}>Spend your EduCoins wisely</Text>

      <LinearGradient
        colors={['#4facfe', '#00f2fe']}
        style={styles.balanceContainer}
      >
        <View>
          <Text style={styles.balanceText}>Your Balance</Text>
          <Text style={styles.balanceAmount}>850</Text>
        </View>
        <TouchableOpacity>
          <Image source={{ uri: 'https://cdn-icons-png.flaticon.com/512/263/263142.png' }} style={styles.cartIcon} />
        </TouchableOpacity>
      </LinearGradient>

      <View style={styles.itemCard}>
        <Image source={{ uri: 'https://cdn-icons-png.flaticon.com/512/224/224598.png' }} style={styles.itemImage} />
        <View style={styles.itemDetails}>
          <Text style={styles.itemName}>Physics Textbook</Text>
          <Text style={styles.itemCategory}>Books</Text>
          <Text style={styles.itemDescription}>Complete guide to quantum mechanics</Text>
        </View>
        <View style={styles.purchaseContainer}>
            <Text style={styles.itemPrice}>250</Text>
            <TouchableOpacity style={styles.purchaseButton}>
                <Text style={styles.purchaseButtonText}>Purchase</Text>
            </TouchableOpacity>
        </View>
      </View>

      <View style={styles.itemCard}>
        <Image source={{ uri: 'https://cdn-icons-png.flaticon.com/512/2906/2906256.png' }} style={styles.itemImage} />
        <View style={styles.itemDetails}>
          <Text style={styles.itemName}>VR Headset Skin</Text>
          <Text style={styles.itemCategory}>VR Gear</Text>
          <Text style={styles.itemDescription}>Holographic blue theme</Text>
        </View>
        <View style={styles.purchaseContainer}>
            <Text style={styles.itemPrice}>500</Text>
            <TouchableOpacity style={styles.purchaseButton}>
                <Text style={styles.purchaseButtonText}>Purchase</Text>
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
    balanceContainer: {
        borderRadius: 15,
        padding: 20,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 20,
    },
    balanceText: {
        color: '#fff',
        fontSize: 16,
    },
    balanceAmount: {
        color: '#fff',
        fontSize: 36,
        fontWeight: 'bold',
    },
    cartIcon: {
        width: 30,
        height: 30,
        tintColor: 'white'
    },
    itemCard: {
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
    itemImage: {
        width: 60,
        height: 60,
        marginRight: 15,
    },
    itemDetails: {
        flex: 1,
    },
    itemName: {
        fontSize: 18,
        fontWeight: 'bold',
    },
    itemCategory: {
        fontSize: 14,
        color: '#6c757d',
    },
    itemDescription: {
        fontSize: 12,
        color: '#6c757d',
        marginTop: 5,
    },
    itemPrice: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#007bff',
        marginBottom: 5
    },
    purchaseButton: {
        backgroundColor: '#00c6ff',
        borderRadius: 20,
        paddingVertical: 5,
        paddingHorizontal: 15,
    },
    purchaseButtonText: {
        color: '#fff',
        fontWeight: 'bold',
        textAlign: 'center'
    },
    purchaseContainer: {
        alignItems: 'center'
    }
});
