const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('Replies with some server info'),
	async execute(interaction) {
		await interaction.reply(`Server info:\nServer name: ${interaction.guild.name}\nTotal members: ${interaction.guild.memberCount}`);
	},
};
