---
name: powershell-xml-processing
description: "Use when processing XML data in PowerShell."
category: software-development
tags: [powershell, xml, parsing, xpath, config]
---
# PowerShell XML Processing

Working with XML data in PowerShell.

## Loading XML

```powershell
# From file
$xml = [xml](Get-Content "config.xml" -Raw)

# From string
$xml = [xml]'<root><item id="1">Value</item></root>'

# From web
$xml = [xml](Invoke-WebRequest -Uri "https://example.com/data.xml").Content
```

## Navigation

```powershell
$xml = [xml]@"
<project>
  <name>MyApp</name>
  <version>1.0.0</version>
  <dependencies>
    <dep id="boost" version="1.84" />
    <dep id="vulkan" version="1.3" />
  </dependencies>
</project>
"@

# Dot-notation
$xml.project.name           # MyApp
$xml.project.dependencies.dep[0].id  # boost

# XPath
$xml.SelectSingleNode("//dep[@id='vulkan']").version
$xml.SelectNodes("//dep") | ForEach-Object { $_.id }
```

## Modifying XML

```powershell
# Add element
$newDep = $xml.CreateElement("dep")
$newDep.SetAttribute("id", "fmt")
$newDep.SetAttribute("version", "10")
$xml.project.dependencies.AppendChild($newDep)

# Modify attribute
$dep = $xml.SelectSingleNode("//dep[@id='boost']")
$dep.SetAttribute("version", "1.85")

# Remove element
$dep = $xml.SelectSingleNode("//dep[@id='vulkan']")
$xml.project.dependencies.RemoveChild($dep)

# Save
$xml.Save("config.xml")
```

## Working with CSProj / .config Files

```powershell
# Read .csproj
$csproj = [xml](Get-Content "MyProject.csproj" -Raw)
$csproj.Project.PropertyGroup | Select-Object TargetFramework, Platform

# Read app.config
$config = [xml](Get-Content "app.config" -Raw)
$config.configuration.connectionStrings.add.connectionString

# Read .vcxproj
$vcxproj = [xml](Get-Content "project.vcxproj" -Raw)
$ns = @{ ns = "http://schemas.microsoft.com/developer/msbuild/2003" }
$vcxproj.SelectNodes("//ns:ClCompile", $ns) | ForEach-Object { $_.Include }
```

## Pitfalls

- **[xml] type accelerator** requires well-formed XML -- wrap in try/catch
- **Namespaces** need explicit handling with SelectSingleNode/SelectNodes
- **XML preserving** -- [xml] parser may reformat whitespace; use XmlWriter for control
- **Large XML** can be memory-intensive -- use XmlReader for streaming (>100MB)
- **Special chars** -- XML &, <, >, ' " need encoding or CDATA sections
