package repo

import (
	"context"
	"fmt"
	"go-srv/internal/entities"
	"time"

	"github.com/jackc/pgx/v4"
	"github.com/jackc/pgx/v4/pgxpool"
)

const insertQuery = `
	insert into response (id, original_text, category) values ($1, $2, $3);
`

type Repo struct {
	pool *pgxpool.Pool
}

func NewRepo(
	ctx context.Context,
	host string,
	port int,
	username string,
	password string,
	dbName string,
) (*Repo, error) {
	repoUrl := fmt.Sprintf("postgres://%s:%s@%s:%d/%s?sslmode=disable",
		username,
		password,
		host,
		port,
		dbName,
	)

	var conn *pgxpool.Pool
	var err error
	for i := 0; i < 30; i++ {
		conn, err = pgxpool.Connect(ctx, repoUrl)
		if err != nil {
			time.Sleep(time.Second)
		} else {
			return &Repo{
				pool: conn,
			}, nil
		}
	}
	return nil, err
}

func (r *Repo) SaveResponses(ctx context.Context, responses []entities.Response) error {
	batch := &pgx.Batch{}
	for _, response := range responses {
		batch.Queue(
			insertQuery,
			response.Id,
			response.OriginalText,
			response.Category,
		)
	}

	br, err := r.pool.Acquire(ctx)
	if err != nil {
		return err
	}
	defer br.Release()

	if err := br.Conn().SendBatch(ctx, batch).Close(); err != nil {
		return err
	}
	return nil
}
