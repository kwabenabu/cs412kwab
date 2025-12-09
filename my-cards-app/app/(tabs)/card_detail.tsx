import React, { useEffect, useState } from 'react';
import { View, Text, Image, StyleSheet, ActivityIndicator } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

const API_URL = 'https://cs-webapps.bu.edu/kwabamp/project/api/cards/';

export default function CardDetailScreen() {
  const { cardId } = useLocalSearchParams();
  const resolvedCardId = Array.isArray(cardId) ? cardId[0] : cardId;
  const [card, setCard] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!resolvedCardId) return;
    setLoading(true);
    fetch(`${API_URL}${resolvedCardId}/`)
      .then((res) => res.json())
      .then((data) => {
        setCard(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [resolvedCardId]);

  if (loading) {
    return <ActivityIndicator size="large" style={{ flex: 1 }} />;
  }
  if (!card) {
    return <Text style={{ flex: 1, textAlign: 'center', marginTop: 40 }}>Card not found.</Text>;
  }

  return (
    <View style={styles.container}>
      {card.image ? (
        <Image source={{ uri: card.image }} style={styles.image} />
      ) : (
        <View style={styles.placeholder} />
      )}
      <Text style={styles.title}>{card.set?.name} #{card.card_number}</Text>
      <Text style={styles.player}>{card.player?.full_name}</Text>
      <Text>Rarity: {card.rarity}</Text>
      <Text>Value: ${card.estimated_value}</Text>
      <Text>Serial: {card.serial_number || 'N/A'}</Text>
      <Text>Created: {card.created_at}</Text>
      <Text>Updated: {card.updated_at}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff', alignItems: 'center', padding: 24 },
  image: { width: 180, height: 270, resizeMode: 'cover', borderRadius: 12, marginBottom: 16 },
  placeholder: { width: 180, height: 270, backgroundColor: '#ddd', borderRadius: 12, marginBottom: 16 },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 8 },
  player: { fontSize: 18, marginBottom: 8 },
});
