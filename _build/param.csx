Info("Expressions: " + string.Join(", ", Model.Expressions.Select(e => e.Name)));
var m = Model.Tables["Market Prices"].Partitions.First().Query;
Info("Source uses parameter: " + (m.IndexOf("SourceFolder") >= 0 ? "YES" : "NO"));
Info("PARAM OK");
