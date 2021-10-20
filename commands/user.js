const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('user')
		.setDescription('Replies with some user info'),
	async execute(interaction) {
		await interaction.reply(`Some info about you:\nYour tag: ${interaction.user.tag}\nYour ID: ${interaction.user.id}`);
	},
};
