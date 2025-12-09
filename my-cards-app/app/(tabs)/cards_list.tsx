import React from 'react';
import { View, Text, FlatList, Image, StyleSheet, Pressable } from 'react-native';
import { useRouter } from 'expo-router';
import { mockCards } from '../../src/mockData';

export default function CardsListScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Soccer Trading Cards</Text>
      <FlatList
        data={mockCards}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <Pressable onPress={() => router.push({ pathname: '/card_detail', params: { cardId: item.id } })} style={styles.card}>
            <Image source={{ uri: item.image }} style={styles.image} />
            <View style={styles.info}>
              <Text style={styles.cardName}>{item.set?.name} #{item.card_number}</Text>
              <Text>{item.player?.full_name}</Text>
              <Text>Rarity: {item.rarity}</Text>
              <Text>Value: ${item.estimated_value}</Text>
            </View>
          </Pressable>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 16 },
  card: { flexDirection: 'row', marginBottom: 16, backgroundColor: '#f9f9f9', borderRadius: 8, overflow: 'hidden', elevation: 2 },
  image: { width: 80, height: 120, resizeMode: 'cover', borderRadius: 8 },
  placeholder: { width: 80, height: 120, backgroundColor: '#ddd', borderRadius: 8 },
  info: { flex: 1, padding: 12, justifyContent: 'center' },
  cardName: { fontWeight: 'bold', fontSize: 16 },
});
