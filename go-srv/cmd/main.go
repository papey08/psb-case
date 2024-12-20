package main

import (
	"context"
	"fmt"
	"go-srv/internal/adapters/classifier_client"
	"go-srv/internal/ports"
	"go-srv/internal/repo"
	"go-srv/internal/services"
	"log"

	"github.com/spf13/viper"
)

func InitConfig() error {
	viper.SetConfigFile("./config.yaml")
	return viper.ReadInConfig()
}

func main() {
	if err := InitConfig(); err != nil {
		log.Fatal(err.Error())
	}
	ctx := context.Background()

	repo, err := repo.NewRepo(ctx,
		viper.GetString("db.host"),
		viper.GetInt("db.port"),
		viper.GetString("db.username"),
		viper.GetString("db.password"),
		viper.GetString("db.dbname"),
	)
	if err != nil {
		log.Fatal(err.Error())
	}

	classifierClient, err := classifier_client.NewClassifierCli(ctx, viper.GetString("classifier.addr"))
	if err != nil {
		log.Fatal(err.Error())
	}

	responsesCollector := services.NewResponsesCollector(classifierClient, repo)

	adminService := services.NewAdminService(repo)
	adminPage := ports.NewAdminPage(adminService)

	log.Println("🎉server started🎉")
	go func() {
		fmt.Println(viper.GetString("admin.addr"))
		adminPage.Run(viper.GetString("admin.addr"))
	}()

	responsesCollector.Run(ctx, 12000000, 1000)
}
