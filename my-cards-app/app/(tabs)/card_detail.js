import React, { useEffect, useState } from 'react';
import { View, Text, Image, ActivityIndicator } from 'react-native';
import { styles } from '../../assets/my_styles';
import { useLocalSearchParams } from 'expo-router';

const API_URL = 'http://10.193.204.31:8000/project/api/cards/';

export default function CardDetailScreen() {
  const { cardId } = useLocalSearchParams();
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!cardId) return;
    fetch(`${API_URL}${cardId}/`)
      .then((res) => res.json())
      .then((data) => {
        setCard(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [cardId]);

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
    </View>
  );
}
