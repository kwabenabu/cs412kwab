import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, ActivityIndicator, Pressable } from 'react-native';
import { styles } from '../../assets/my_styles';
import { useRouter } from 'expo-router';

const API_URL = 'http://10.193.204.31:8000/project/api/cards/';

export default function CardsListScreen() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setCards(data.results || data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <ActivityIndicator size="large" style={{ flex: 1 }} />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Soccer Trading Cards</Text>
      <FlatList
        data={cards}
        keyExtractor={(item) => item.id?.toString() || item.pk?.toString()}
        renderItem={({ item }) => (
          <Pressable onPress={() => router.push({ pathname: '/card_detail', params: { cardId: item.id } })} style={styles.card}>
            {item.image ? (
              <Image source={{ uri: item.image }} style={styles.image} />
            ) : (
              <View style={styles.placeholder} />
            )}
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
