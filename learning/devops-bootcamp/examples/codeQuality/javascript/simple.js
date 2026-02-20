module.exports = {
	simpleTest: function()
	{
		return 1;
	},
	addTwo: function(p1, p2)
	{
		return p1 + p2;
	},
	multTwo: function(p1, p2)
	{
		return p1 * p2;
	},
	subTwo: function(p1, p2)
	{
		return p1 - p2;
	},
	divTwo: function(p1, p2)
	{
		if (p2 == 0)
		{
			return 0;
		}
		else
		{
			return p1 / p2;
		}
	}

}
