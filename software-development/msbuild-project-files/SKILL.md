---
name: msbuild-project-files
description: "Use when editing .csproj/.vcxproj MSBuild XML."
category: software-development
tags: [msbuild, csproj, vcxproj, xml, project-files]
---
# MSBuild Project Files

Editing and understanding MSBuild project files (.csproj, .vcxproj).

## .csproj (C#/.NET) Structure

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <OutputType>Exe</OutputType>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <Platforms>x64;x86</Platforms>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <ProjectReference Include="..\Core\Core.csproj" />
  </ItemGroup>

  <ItemGroup>
    <Content Include="appsettings.json">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </Content>
  </ItemGroup>
</Project>
```

## .vcxproj (C++) Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
    <ProjectConfiguration Include="Debug|x64">
      <Configuration>Debug</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|x64">
      <Configuration>Release</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
  </ItemGroup>

  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />

  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseOfMfc>false</UseOfMfc>
    <PlatformToolset>v143</PlatformToolset>
  </PropertyGroup>

  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />

  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <Optimization>MaxSpeed</Optimization>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <PreprocessorDefinitions>NDEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>
      <WarningLevel>Level3</WarningLevel>
      <LanguageStandard>stdcpp20</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
    </Link>
  </ItemDefinitionGroup>

  <ItemGroup>
    <ClCompile Include="main.cpp" />
    <ClCompile Include="utils.cpp" />
  </ItemGroup>
  <ItemGroup>
    <ClInclude Include="utils.h" />
  </ItemGroup>

  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
</Project>
```

## Common MSBuild Properties

```xml
<PropertyGroup>
  <!-- Output -->
  <OutputPath>bin\$(Configuration)\</OutputPath>
  <IntermediateOutputPath>obj\$(Configuration)\</IntermediateOutputPath>

  <!-- C++ specific -->
  <ConfigurationType>Application</ConfigurationType>   <!-- or DynamicLibrary, StaticLibrary -->
  <PlatformToolset>v143</PlatformToolset>
  <WindowsTargetPlatformVersion>10.0</WindowsTargetPlatformVersion>

  <!-- C# specific -->
  <TargetFramework>net8.0</TargetFramework>
  <Nullable>enable</Nullable>
  <ImplicitUsings>enable</ImplicitUsings>
</PropertyGroup>
```

## Conditions

```xml
<PropertyGroup Condition="'$(Configuration)' == 'Debug'">
  <Optimize>false</Optimize>
</PropertyGroup>

<PropertyGroup Condition="'$(Configuration)' == 'Release'">
  <Optimize>true</Optimize>
</PropertyGroup>

<ItemGroup Condition="'$(TargetFramework)' == 'net48'">
  <PackageReference Include="System.Text.Json" Version="8.0.0" />
</ItemGroup>
```

## Custom Targets

```xml
<Target Name="PostBuild" AfterTargets="Build">
  <Copy SourceFiles="$(OutputPath)$(AssemblyName).dll"
        DestinationFolder="C:\Deploy\" />
</Target>

<Target Name="GenerateVersion" BeforeTargets="BeforeBuild">
  <WriteLinesToFile File="version.txt"
                    Lines="$([System.DateTime]::Now.ToString('yyyy.MM.dd'))"
                    Overwrite="true" />
</Target>
