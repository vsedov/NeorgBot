const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('wiki')
		.setDescription('Replies with the link to the Neorg wiki'),
	async execute(interaction) {
		await interaction.reply(`Link to neorg wiki:\nhttps://github.com/nvim-neorg/neorg/wiki`);
	},
};
