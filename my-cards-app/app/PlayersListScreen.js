import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, StyleSheet, ActivityIndicator } from 'react-native';

const API_URL = 'http://10.193.204.31:8000/project/api/players/';

export default function PlayersListScreen() {
	const [players, setPlayers] = useState([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		fetch(API_URL)
			.then((res) => res.json())
			.then((data) => {
				setPlayers(data.results || data);
				setLoading(false);
			})
			.catch(() => setLoading(false));
	}, []);

	if (loading) {
		return <ActivityIndicator size="large" style={{ flex: 1 }} />;
	}

	return (
		<View style={styles.container}>
			<Text style={styles.title}>Players</Text>
			<FlatList
				data={players}
				keyExtractor={(item) => item.id?.toString() || item.pk?.toString()}
				renderItem={({ item }) => (
					<View style={styles.player}>
						{item.image ? (
							<Image source={{ uri: item.image }} style={styles.image} />
						) : (
							<View style={styles.placeholder} />
						)}
						<View style={styles.info}>
							<Text style={styles.name}>{item.full_name}</Text>
							<Text>{item.position} - {item.club_team}</Text>
							<Text>{item.country}</Text>
						</View>
					</View>
				)}
			/>
		</View>
	);
}

const styles = StyleSheet.create({
	container: { flex: 1, backgroundColor: '#fff', padding: 16 },
	title: { fontSize: 24, fontWeight: 'bold', marginBottom: 16 },
	player: { flexDirection: 'row', marginBottom: 16, backgroundColor: '#f9f9f9', borderRadius: 8, overflow: 'hidden', elevation: 2 },
	image: { width: 80, height: 80, resizeMode: 'cover', borderRadius: 40 },
	placeholder: { width: 80, height: 80, backgroundColor: '#ddd', borderRadius: 40 },
	info: { flex: 1, padding: 12, justifyContent: 'center' },
	name: { fontWeight: 'bold', fontSize: 16 },
});

