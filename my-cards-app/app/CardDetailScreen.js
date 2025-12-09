import React, { useEffect, useState } from 'react';
import { View, Text, Image, StyleSheet, ActivityIndicator } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

const API_URL = 'http://10.193.204.31:8000/project/card/';

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

