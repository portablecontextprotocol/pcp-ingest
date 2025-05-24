Skip to main content
![Sui Docs Logo](https://docs.sui.io/img/sui-logo.svg)
**Sui Documentation**
GuidesConceptsStandardsReferences
Search`⌘``K`
  * Overview
  * Developer Guides
    * Getting Started
      * Install Sui
      * Connect to a Sui Network
      * Connect to a Local Network
      * Get Sui Address
      * Get SUI Tokens
      * Access Sui Data
    * Your First Sui dApp
    * Sui 101
    * Coins and Tokens
    * Stablecoins
    * NFTs
    * Cryptography
    * Advanced Topics
    * App Examples
      * Distributed Counter
      * Trustless Swap
      * Coin Flip
      * Review Rating
      * Blackjack
      * Plinko
      * Tic-Tac-Toe
      * Oracles
    * Dev Cheat Sheet
  * Operator Guides


  *   * Developer Guides
  * App Examples
  * Tic-Tac-Toe


On this page
# Tic-Tac-Toe
🧠Expected effort
This guide is rated as basic.
You can expect basic guides to take 30-45 minutes of dedicated time. The length of time necessary to fully understand some of the concepts raised in this guide might increase this estimate.
You can view the complete source code for this app example in the Sui repository.
This guide covers three different implementations of the game tic-tac-toe on Sui. The first example utilizes a centralized admin that owns the board object and marks it on the users’ behalf. The second example utilizes a shared object that both users can mutate. And the third example utilizes a multisig, where instead of sharing the game board, it's in a 1-of-2 multisig of both users’ accounts.
The guide is divided into three parts that each cover a different implementation of the tic-tac-toe game board:
  1. Centralized game board: An admin service that tracks player moves and updates the game board.
  2. Shared game board: A shared object that allows players to directly update the game board.
  3. Multisig operated game board: A multisig account that acts as the game admin, allowing either player to update the game board directly.


## What the guide teaches​
  * **Owned objects:** The guide teaches you how to use owned objects, in this case to act as the game board in the centralized and multisig version of tic-tac-toe. Owned objects are objects that are owned by a single account and can only be modified by that account. In this case, the game board is owned by a game admin, who is responsible for updating the board with each player's move.
  * **Shared objects:** The guide teaches you how to use shared objects, in this case to act as the game board in the more decentralized version of tic-tac-toe. Shared objects are objects that can be modified by multiple accounts. In this case, the game board is shared between the two players, allowing them to update the board directly.
  * **Multisig accounts:** The guide teaches you how to use multisig accounts to share ownership of the game board between two players. Multisig accounts are accounts that require a certain threshold of signatures to authorize a transaction. In this case, the game board is owned by a 1-of-2 multisig account.
  * **Dynamic object fields:** The guide teaches you how to use dynamic object fields, in this case to transfer the actions of the players to the game board, which will be retrieved by the game admin. See The Move Book to learn more about dynamic object fields.


## What you need​
Before getting started, make sure you have:
  * Installed the latest version of Sui.
  * Read the basics of shared versus owned objects.


## Directory structure​
To begin, create a new folder on your system titled `tic-tac-toe` that holds all your files.
In this folder, create the following subfolders:
  * `move` to hold the Move code for the game board.
    * `sources` to hold the Move source files.


Click to open
Add `Move.toml` to `tic-tac-toe/move/`
examples/tic-tac-toe/move/Move.toml
```
[package]  
name="tic_tac_toe"  
edition="2024.beta"  
  
[dependencies]  
Sui={git="https://github.com/MystenLabs/sui.git",subdir="crates/sui-framework/packages/sui-framework",rev="framework/testnet"}  
  
[addresses]  
tic_tac_toe="0x0"  

```

CHECKPOINT
  * You have the latest version of Sui installed. If you run `sui --version` in your terminal or console, it responds with the currently installed version.
  * You have a directory to place the files you create in.
  * You have created a `Move.toml` file in the `tic-tac-toe/move/` directory.


## owned.move​
Create a new file in `tic-tac-toe/move/sources` titled `owned.move`. Later, you will update this file to contain the Move code for the game board in the centralized (and multisig) version of tic-tac-toe.
In this first example of tic-tac-toe, the `Game` object, including the game board, is controlled by a game admin.
examples/tic-tac-toe/move/sources/owned.move
```
publicstruct Gamehaskey, store {  
id: UID,  
board: vector<u8>,  
turn: u8,  
x: address,  
o: address,  
admin: vector<u8>,  
}  

```

Ignore the `admin` field for now, as it is only relevant for the multisig approach.
Games are created with the `new` function:
examples/tic-tac-toe/move/sources/owned.move
```
publicfunnew(x: address, o: address, admin: vector<u8>, ctx: &mut TxContext): Game {  
letgame = Game {  
id: object::new(ctx),  
board: vector[MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__],  
turn: 0,  
        x,  
        o,  
        admin,  
    };  
  
letturn = TurnCap {  
id: object::new(ctx),  
game: object::id(&game),  
    };  
  
    transfer::transfer(turn, x);  
    game  
}  

```

Some things to note:
  * `MARK__` is a constant that represents an empty cell on the game board. `MARK_X` and `MARK_O` represent the two players' markers.
  * The first player is sent a `TurnCap`, which gives them permission to take the next turn.
  * This function creates and returns the `Game` object, it is up to its creator to send it to the game admin to own.


Because the players don’t own the game board object, they cannot directly mutate it. Instead, they indicate their move by creating a `Mark` object with their intended placement and send it to the game object using transfer to object:
examples/tic-tac-toe/move/sources/owned.move
```
publicstruct Markhaskey, store {  
id: UID,  
player: address,  
row: u8,  
col: u8,  
}  

```

When playing the game, the admin operates a service that keeps track of marks using events. When a request is received (`send_mark`), the admin tries to place the marker on the board (`place_mark`). Each move requires two steps (thus two transactions): one from the player and one from the admin. This setup relies on the admin's service to keep the game moving.
examples/tic-tac-toe/move/sources/owned.move
```
publicfunsend_mark(cap: TurnCap, row: u8, col: u8, ctx: &mut TxContext) {  
assert!(row < 3 && col < 3, EInvalidLocation);  
  
let TurnCap { id, game } = cap;  
    id.delete();  
  
letmark = Mark {  
id: object::new(ctx),  
player: ctx.sender(),  
        row,  
        col,  
    };  
  
    event::emit(MarkSent { game, mark: object::id(&mark) });  
    transfer::transfer(mark, game.to_address());  
}  
  
publicfunplace_mark(game: &mut Game, mark: Receiving<Mark>, ctx: &mut TxContext) {  
assert!(game.ended() == TROPHY_NONE, EAlreadyFinished);  
  
let Mark { id, row, col, player } = transfer::receive(&mut game.id, mark);  
    id.delete();  
  
let (me, them, sentinel) = game.next_player();  
assert!(me == player, EWrongPlayer);  
  
if (game[row, col] == MARK__) {  
        *(&mut game[row, col]) = sentinel;  
        game.turn = game.turn + 1;  
    };  
  
letend = game.ended();  
if (end == TROPHY_WIN) {  
        transfer::transfer(game.mint_trophy(end, them, ctx), me);  
        event::emit(GameEnd { game: object::id(game) });  
    } else if (end == TROPHY_DRAW) {  
        transfer::transfer(game.mint_trophy(end, them, ctx), me);  
        transfer::transfer(game.mint_trophy(end, me, ctx), them);  
        event::emit(GameEnd { game: object::id(game) });  
    } else if (end == TROPHY_NONE) {  
letcap = TurnCap { id: object::new(ctx), game: object::id(game) };  
let (to, _, _) = game.next_player();  
        transfer::transfer(cap, to);  
    } else {  
abortEInvalidEndState  
    }  
}  

```

When a player sends a mark, a `Mark` object is created and is sent to the `Game` object. The admin then receives the mark and places it on the board. This is a use of dynamic object fields, where an object, `Game`, can hold other objects, `Mark`.
To view the entire source code, see the owned.move source file. You can find the rest of the logic, including how to check for a winner, as well as deleting the game board after the game concludes there.
Click to open
`owned.move`
examples/tic-tac-toe/move/sources/owned.move
```
/// An implementation of Tic Tac Toe, using owned objects.  
///  
/// The `Game` object is owned by an admin, so players cannot mutate the game  
/// board directly. Instead, they convey their intention to place a mark by  
/// transferring a `Mark` object to the `Game`.  
///  
/// This means that every move takes two owned object fast path operations --  
/// one by the player, and one by the admin. The admin could be a third party  
/// running a centralized service that monitors marker placement events and  
/// responds to them, or it could be a 1-of-2 multisig address shared between  
/// the two players, as demonstrated in the demo app.  
///  
/// The `shared` module shows a variant of this game implemented using shared  
/// objects, which provides different trade-offs: Using shared objects is more  
/// expensive, however the implementation is more straightforward and each move  
/// only requires one transaction.  
module tic_tac_toe::owned;  
  
usesui::{event, transfer::Receiving};  
  
// === Object Types ===  
  
/// The state of an active game of tic-tac-toe.  
publicstruct Gamehaskey, store {  
id: UID,  
/// Marks on the board.  
board: vector<u8>,  
/// The next turn to be played.  
turn: u8,  
/// The address expected to send moves on behalf of X.  
x: address,  
/// The address expected to send moves on behalf of O.  
o: address,  
/// Public key of the admin address.  
admin: vector<u8>,  
}  
  
/// The player that the next turn is expected from is given a `TurnCap`.  
publicstruct TurnCaphaskey {  
id: UID,  
game: ID,  
}  
  
/// A request to make a play -- only the player with the `TurnCap` can  
/// create and send `Mark`s.  
publicstruct Markhaskey, store {  
id: UID,  
player: address,  
row: u8,  
col: u8,  
}  
  
/// An NFT representing a finished game. Sent to the winning player if there  
/// is one, or to both players in the case of a draw.  
publicstruct Trophyhaskey {  
id: UID,  
/// Whether the game was won or drawn.  
status: u8,  
/// The state of the board at the end of the game.  
board: vector<u8>,  
/// The number of turns played  
turn: u8,  
/// The other player (relative to the player who owns this Trophy).  
other: address,  
}  
  
// === Event Types ===  
  
publicstruct MarkSenthascopy, drop {  
game: ID,  
mark: ID,  
}  
  
publicstruct GameEndhascopy, drop {  
game: ID,  
}  
  
// === Constants ===  
  
// Marks  
constMARK__: u8 = 0;  
constMARK_X: u8 = 1;  
constMARK_O: u8 = 2;  
  
// Trophy status  
constTROPHY_NONE: u8 = 0;  
constTROPHY_DRAW: u8 = 1;  
constTROPHY_WIN: u8 = 2;  
  
// === Errors ===  
  
#[error]  
constEInvalidLocation: vector<u8> = b"Movewasforapositionthatdoesn'texistontheboard";  
  
#[error]  
constEWrongPlayer: vector<u8> = b"Gameexpectedamovefromanotherplayer";  
  
#[error]  
constENotFinished: vector<u8> = b"Gamehasnotreachedanendcondition";  
  
#[error]  
constEAlreadyFinished: vector<u8> = b"Can'tplaceamarkonafinishedgame";  
  
#[error]  
constEInvalidEndState: vector<u8> = b"Gamereachedanendstatethatwasn'texpected";  
  
// === Public Functions ===  
  
/// Create a new game, played by `x` and `o`. The game should be  
/// transfered to the address that will administrate the game. If  
/// that address is a multi-sig of the two players, its public key  
/// should be passed as `admin`.  
publicfunnew(x: address, o: address, admin: vector<u8>, ctx: &mut TxContext): Game {  
letgame = Game {  
id: object::new(ctx),  
board: vector[MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__],  
turn: 0,  
				x,  
				o,  
				admin,  
		};  
  
letturn = TurnCap {  
id: object::new(ctx),  
game: object::id(&game),  
		};  
  
// X is the first player, so send the capability to them.  
		transfer::transfer(turn, x);  
		game  
}  
  
/// Called by the active player to express their intention to make a move.  
/// This consumes the `TurnCap` to prevent a player from making more than  
/// one move on their turn.  
publicfunsend_mark(cap: TurnCap, row: u8, col: u8, ctx: &mut TxContext) {  
assert!(row < 3 && col < 3, EInvalidLocation);  
  
let TurnCap { id, game } = cap;  
		id.delete();  
  
letmark = Mark {  
id: object::new(ctx),  
player: ctx.sender(),  
				row,  
				col,  
		};  
  
		event::emit(MarkSent { game, mark: object::id(&mark) });  
		transfer::transfer(mark, game.to_address());  
}  
  
/// Called by the admin (who owns the `Game`), to commit a player's  
/// intention to make a move. If the game should end, `Trophy`s are sent to  
/// the appropriate players, if the game should continue, a new `TurnCap` is  
/// sent to the player who should make the next move.  
publicfunplace_mark(game: &mut Game, mark: Receiving<Mark>, ctx: &mut TxContext) {  
assert!(game.ended() == TROPHY_NONE, EAlreadyFinished);  
  
// Fetch the mark on behalf of the game -- only works if the mark in  
// question was sent to this game.  
let Mark { id, row, col, player } = transfer::receive(&mut game.id, mark);  
		id.delete();  
  
// Confirm that the mark is from the player we expect -- it should not  
// be possible to hit this assertion, because the `Mark`s can only be  
// created by the address that owns the `TurnCap` which cannot be  
// transferred, and is always held by `game.next_player()`.  
let (me, them, sentinel) = game.next_player();  
assert!(me == player, EWrongPlayer);  
  
if (game[row, col] == MARK__) {  
				*(&mut game[row, col]) = sentinel;  
				game.turn = game.turn + 1;  
		};  
  
// Check win condition -- if there is a winner, send them the trophy,  
// otherwise, create a new turn cap and send that to the next player.  
letend = game.ended();  
if (end == TROPHY_WIN) {  
				transfer::transfer(game.mint_trophy(end, them, ctx), me);  
				event::emit(GameEnd { game: object::id(game) });  
		} else if (end == TROPHY_DRAW) {  
				transfer::transfer(game.mint_trophy(end, them, ctx), me);  
				transfer::transfer(game.mint_trophy(end, me, ctx), them);  
				event::emit(GameEnd { game: object::id(game) });  
		} else if (end == TROPHY_NONE) {  
letcap = TurnCap { id: object::new(ctx), game: object::id(game) };  
let (to, _, _) = game.next_player();  
				transfer::transfer(cap, to);  
		} else {  
abortEInvalidEndState  
		}  
}  
  
publicfunburn(game: Game) {  
assert!(game.ended() != TROPHY_NONE, ENotFinished);  
let Game { id, .. } = game;  
		id.delete();  
}  
  
/// Test whether the game has reached an end condition or not.  
publicfunended(game: &Game): u8 {  
if (// Test rows  
test_triple(game, 0, 1, 2) ||  
test_triple(game, 3, 4, 5) ||  
test_triple(game, 6, 7, 8) ||  
// Test columns  
test_triple(game, 0, 3, 6) ||  
test_triple(game, 1, 4, 7) ||  
test_triple(game, 2, 5, 8) ||  
// Test diagonals  
test_triple(game, 0, 4, 8) ||  
test_triple(game, 2, 4, 6)) {  
				TROPHY_WIN  
		} else if (game.turn == 9) {  
				TROPHY_DRAW  
		} else {  
				TROPHY_NONE  
		}  
}  
  
#[syntax(index)]  
publicfunmark(game: &Game, row: u8, col: u8): &u8 {  
		&game.board[(row * 3 + col) as u64]  
}  
  
#[syntax(index)]  
funmark_mut(game: &mut Game, row: u8, col: u8): &mutu8 {  
		&mut game.board[(row * 3 + col) as u64]  
}  
  
// === Private Helpers ===  
  
/// Address of the player the move is expected from, the address of the  
/// other player, and the mark to use for the upcoming move.  
funnext_player(game: &Game): (address, address, u8) {  
if (game.turn % 2 == 0) {  
				(game.x, game.o, MARK_X)  
		} else {  
				(game.o, game.x, MARK_O)  
		}  
}  
  
/// Test whether the values at the triple of positions all match each other  
/// (and are not all EMPTY).  
funtest_triple(game: &Game, x: u8, y: u8, z: u8): bool {  
letx = game.board[x as u64];  
lety = game.board[y as u64];  
letz = game.board[z as u64];  
  
		MARK__ != x && x == y && y == z  
}  
  
/// Create a trophy from the current state of the `game`, that indicates  
/// that a player won or drew against `other` player.  
funmint_trophy(game: &Game, status: u8, other: address, ctx: &mut TxContext): Trophy {  
		Trophy {  
id: object::new(ctx),  
				status,  
board: game.board,  
turn: game.turn,  
				other,  
		}  
}  
  
// === Test Helpers ===  
#[test_only]  
publicusefungame_boardas Game.board;  
#[test_only]  
publicusefuntrophy_statusas Trophy.status;  
#[test_only]  
publicusefuntrophy_boardas Trophy.board;  
#[test_only]  
publicusefuntrophy_turnas Trophy.turn;  
#[test_only]  
publicusefuntrophy_otheras Trophy.other;  
  
#[test_only]  
publicfungame_board(game: &Game): vector<u8> {  
		game.board  
}  
  
#[test_only]  
publicfuntrophy_status(trophy: &Trophy): u8 {  
		trophy.status  
}  
  
#[test_only]  
publicfuntrophy_board(trophy: &Trophy): vector<u8> {  
		trophy.board  
}  
  
#[test_only]  
publicfuntrophy_turn(trophy: &Trophy): u8 {  
		trophy.turn  
}  
  
#[test_only]  
publicfuntrophy_other(trophy: &Trophy): address {  
		trophy.other  
}  

```

An alternative version of this game, shared tic-tac-toe, uses shared objects for a more straightforward implementation that doesn't use a centralized service. This comes at a slightly increased cost, as using shared objects is more expensive than transactions involving wholly owned objects.
## shared.move​
In the previous version, the admin owned the game object, preventing players from directly changing the gameboard, as well as requiring two transactions for each marker placement. In this version, the game object is a shared object, allowing both players to access and modify it directly, enabling them to place markers in just one transaction. However, using a shared object generally incurs extra costs because Sui needs to sequence the operations from different transactions. In the context of this game, where players are expected to take turns, this shouldn't significantly impact performance. Overall, this shared object approach simplifies the implementation compared to the previous method.
As the following code demonstrates, the `Game` object in this example is almost identical to the one before it. The only differences are that it does not include an `admin` field, which is only relevant for the multisig version of the game, and it does not have `store`, because it only ever exists as a shared object (so it cannot be transferred or wrapped).
examples/tic-tac-toe/move/sources/shared.move
```
publicstruct Gamehaskey {  
id: UID,  
board: vector<u8>,  
turn: u8,  
x: address,  
o: address,  
}  

```

Take a look at the `new` function:
examples/tic-tac-toe/move/sources/shared.move
```
publicfunnew(x: address, o: address, ctx: &mut TxContext) {  
    transfer::share_object(Game {  
id: object::new(ctx),  
board: vector[MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__],  
turn: 0,  
        x,  
        o,  
    });  
}  

```

Instead of the game being sent to the game admin, it is instantiated as a shared object. The other notable difference is that there is no need to mint a `TurnCap` because the only two addresses that can play this game are `x` and `o`, and this is checked in the next function, `place_mark`:
examples/tic-tac-toe/move/sources/shared.move
```
publicfunplace_mark(game: &mut Game, row: u8, col: u8, ctx: &mut TxContext) {  
assert!(game.ended() == TROPHY_NONE, EAlreadyFinished);  
assert!(row < 3 && col < 3, EInvalidLocation);  
  
let (me, them, sentinel) = game.next_player();  
assert!(me == ctx.sender(), EWrongPlayer);  
  
if (game[row, col] != MARK__) {  
abortEAlreadyFilled  
    };  
  
    *(&mut game[row, col]) = sentinel;  
    game.turn = game.turn + 1;  
  
letend = game.ended();  
if (end == TROPHY_WIN) {  
        transfer::transfer(game.mint_trophy(end, them, ctx), me);  
    } else if (end == TROPHY_DRAW) {  
        transfer::transfer(game.mint_trophy(end, them, ctx), me);  
        transfer::transfer(game.mint_trophy(end, me, ctx), them);  
    } else if (end != TROPHY_NONE) {  
abortEInvalidEndState  
    }  
}  

```

Click to open
`shared.move`
examples/tic-tac-toe/move/sources/shared.move
```
/// An implementation of Tic Tac Toe, using shared objects.  
///  
/// The `Game` object is shared so both players can mutate it, and  
/// contains authorization logic to only accept a move from the  
/// correct player.  
///  
/// The `owned` module shows a variant of this game implemented using  
/// only fast path transactions, which should be cheaper and lower  
/// latency, but either requires a centralized service or a multi-sig  
/// set-up to own the game.  
module tic_tac_toe::shared;  
  
/// The state of an active game of tic-tac-toe.  
publicstruct Gamehaskey {  
id: UID,  
/// Marks on the board.  
board: vector<u8>,  
/// The next turn to be played.  
turn: u8,  
/// The address expected to send moves on behalf of X.  
x: address,  
/// The address expected to send moves on behalf of O.  
o: address,  
}  
  
/// An NFT representing a finished game. Sent to the winning player if there  
/// is one, or to both players in the case of a draw.  
publicstruct Trophyhaskey {  
id: UID,  
/// Whether the game was won or drawn.  
status: u8,  
/// The state of the board at the end of the game.  
board: vector<u8>,  
/// The number of turns played  
turn: u8,  
/// The other player (relative to the player who owns this Trophy).  
other: address,  
}  
  
// === Constants ===  
  
// Marks  
constMARK__: u8 = 0;  
constMARK_X: u8 = 1;  
constMARK_O: u8 = 2;  
  
// Trophy status  
constTROPHY_NONE: u8 = 0;  
constTROPHY_DRAW: u8 = 1;  
constTROPHY_WIN: u8 = 2;  
  
// === Errors ===  
  
#[error]  
constEInvalidLocation: vector<u8> = b"Movewasforapositionthatdoesn'texistontheboard.";  
  
#[error]  
constEWrongPlayer: vector<u8> = b"Gameexpectedamovefromanotherplayer";  
  
#[error]  
constEAlreadyFilled: vector<u8> = b"Attemptedtoplaceamarkonafilledslot.";  
  
#[error]  
constENotFinished: vector<u8> = b"Gamehasnotreachedanendcondition.";  
  
#[error]  
constEAlreadyFinished: vector<u8> = b"Can'tplaceamarkonafinishedgame.";  
  
#[error]  
constEInvalidEndState: vector<u8> = b"Gamereachedanendstatethatwasn'texpected.";  
  
// === Public Functions ===  
  
/// Create a new game, played by `x` and `o`. This function should be called  
/// by the address responsible for administrating the game.  
publicfunnew(x: address, o: address, ctx: &mut TxContext) {  
		transfer::share_object(Game {  
id: object::new(ctx),  
board: vector[MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__, MARK__],  
turn: 0,  
				x,  
				o,  
		});  
}  
  
/// Called by the next player to add a new mark.  
publicfunplace_mark(game: &mut Game, row: u8, col: u8, ctx: &mut TxContext) {  
assert!(game.ended() == TROPHY_NONE, EAlreadyFinished);  
assert!(row < 3 && col < 3, EInvalidLocation);  
  
// Confirm that the mark is from the player we expect.  
let (me, them, sentinel) = game.next_player();  
assert!(me == ctx.sender(), EWrongPlayer);  
  
if (game[row, col] != MARK__) {  
abortEAlreadyFilled  
		};  
  
		*(&mut game[row, col]) = sentinel;  
		game.turn = game.turn + 1;  
  
// Check win condition -- if there is a winner, send them the trophy.  
letend = game.ended();  
if (end == TROPHY_WIN) {  
				transfer::transfer(game.mint_trophy(end, them, ctx), me);  
		} else if (end == TROPHY_DRAW) {  
				transfer::transfer(game.mint_trophy(end, them, ctx), me);  
				transfer::transfer(game.mint_trophy(end, me, ctx), them);  
		} else if (end != TROPHY_NONE) {  
abortEInvalidEndState  
		}  
}  
  
// === Private Helpers ===  
  
/// Address of the player the move is expected from, the address of the  
/// other player, and the mark to use for the upcoming move.  
funnext_player(game: &Game): (address, address, u8) {  
if (game.turn % 2 == 0) {  
				(game.x, game.o, MARK_X)  
		} else {  
				(game.o, game.x, MARK_O)  
		}  
}  
  
/// Test whether the values at the triple of positions all match each other  
/// (and are not all EMPTY).  
funtest_triple(game: &Game, x: u8, y: u8, z: u8): bool {  
letx = game.board[x as u64];  
lety = game.board[y as u64];  
letz = game.board[z as u64];  
  
		MARK__ != x && x == y && y == z  
}  
  
/// Create a trophy from the current state of the `game`, that indicates  
/// that a player won or drew against `other` player.  
funmint_trophy(game: &Game, status: u8, other: address, ctx: &mut TxContext): Trophy {  
		Trophy {  
id: object::new(ctx),  
				status,  
board: game.board,  
turn: game.turn,  
				other,  
		}  
}  
  
publicfunburn(game: Game) {  
assert!(game.ended() != TROPHY_NONE, ENotFinished);  
let Game { id, .. } = game;  
		id.delete();  
}  
  
/// Test whether the game has reached an end condition or not.  
publicfunended(game: &Game): u8 {  
if (// Test rows  
test_triple(game, 0, 1, 2) ||  
test_triple(game, 3, 4, 5) ||  
test_triple(game, 6, 7, 8) ||  
// Test columns  
test_triple(game, 0, 3, 6) ||  
test_triple(game, 1, 4, 7) ||  
test_triple(game, 2, 5, 8) ||  
// Test diagonals  
test_triple(game, 0, 4, 8) ||  
test_triple(game, 2, 4, 6)) {  
				TROPHY_WIN  
		} else if (game.turn == 9) {  
				TROPHY_DRAW  
		} else {  
				TROPHY_NONE  
		}  
}  
  
#[syntax(index)]  
publicfunmark(game: &Game, row: u8, col: u8): &u8 {  
		&game.board[(row * 3 + col) as u64]  
}  
  
#[syntax(index)]  
funmark_mut(game: &mut Game, row: u8, col: u8): &mutu8 {  
		&mut game.board[(row * 3 + col) as u64]  
}  
  
// === Test Helpers ===  
#[test_only]  
publicusefungame_boardas Game.board;  
#[test_only]  
publicusefuntrophy_statusas Trophy.status;  
#[test_only]  
publicusefuntrophy_boardas Trophy.board;  
#[test_only]  
publicusefuntrophy_turnas Trophy.turn;  
#[test_only]  
publicusefuntrophy_otheras Trophy.other;  
  
#[test_only]  
publicfungame_board(game: &Game): vector<u8> {  
		game.board  
}  
  
#[test_only]  
publicfuntrophy_status(trophy: &Trophy): u8 {  
		trophy.status  
}  
  
#[test_only]  
publicfuntrophy_board(trophy: &Trophy): vector<u8> {  
		trophy.board  
}  
  
#[test_only]  
publicfuntrophy_turn(trophy: &Trophy): u8 {  
		trophy.turn  
}  
  
#[test_only]  
publicfuntrophy_other(trophy: &Trophy): address {  
		trophy.other  
}  

```

## Multisig​
Multisig tic-tac-toe uses the same Move code as the owned version of the game, but interacts with it differently. Instead of transferring the game to a third party admin account, the players create a 1-of-2 multisig account to act as the game admin, so that either player can sign on behalf of the "admin". This pattern offers a way to share a resource between up to ten accounts without relying on consensus.
In this implementation of the game, the game is in a 1-of-2 multisig account that acts as the game admin. In this particular case, because there are only two players, the previous example is a more convenient use case. However, this example illustrates that in some cases, a multisig can replace shared objects, thus allowing transactions to bypass consensus when using such an implementation.
### Creating a multisig account​
A multisig account is defined by the public keys of its constituent keypairs, their relative weights, and the threshold -- a signature is valid if the sum of weights of constituent keys having signed the signature exceeds the threshold. In our case, there are at most two constituent keypairs, they each have a weight of 1 and the threshold is also 1. A multisig cannot mention the same public key twice, so keys are deduplicated before the multisig is formed to deal with the case where a player is playing themselves:
examples/tic-tac-toe/ui/src/MultiSig.ts
```
exportfunctionmultiSigPublicKey(keys:PublicKey[]):MultiSigPublicKey{  
const deduplicated:{[key:string]:PublicKey}={};  
for(const key of keys){  
    deduplicated[key.toSuiAddress()]= key;  
}  
  
returnMultiSigPublicKey.fromPublicKeys({  
    threshold:1,  
    publicKeys:Object.values(deduplicated).map((publicKey)=>{  
return{ publicKey, weight:1};  
}),  
});  
}  

```

Click to open
`MultiSig.ts`
examples/tic-tac-toe/ui/src/MultiSig.ts
```
import{PublicKey}from'@mysten/sui/cryptography';  
import{MultiSigPublicKey}from'@mysten/sui/multisig';  
  
/**  
 * Generate the public key corresponding to a 1-of-N multi-sig  
 * composed of `keys` (all with equal weighting).  
 */  
exportfunctionmultiSigPublicKey(keys:PublicKey[]):MultiSigPublicKey{  
// Multi-sig addresses cannot contain the same public keys multiple  
// times. In our case, it's fine to de-duplicate them because all  
// keys get equal weight and the threshold is 1.  
const deduplicated:{[key:string]:PublicKey}={};  
for(const key of keys){  
		deduplicated[key.toSuiAddress()]= key;  
}  
  
returnMultiSigPublicKey.fromPublicKeys({  
		threshold:1,  
		publicKeys:Object.values(deduplicated).map((publicKey)=>{  
return{ publicKey, weight:1};  
}),  
});  
}  

```

Note that an address on Sui can be derived from a public key (this fact is used in the previous example to deduplicate public keys based on their accompanying address), but the opposite is not true. This means that to start a game of multisig tic-tac-toe, players must exchange public keys, instead of addresses.
### Building a multisig transaction​
When creating a multisig game, we make use of `owned::Game`'s `admin` field to store the multisig public key for the admin account. Later, it will be used to form the signature for the second transaction in the move. This does not need to be stored on-chain, but we are doing so for convenience so that when we fetch the `Game`'s contents, we get the public key as well:
examples/tic-tac-toe/ui/src/hooks/useTransactions.ts
```
newMultiSigGame(player:PublicKey, opponent:PublicKey):Transaction{  
const admin =multiSigPublicKey([player, opponent]);  
const tx =newTransaction();  
  
const game = tx.moveCall({  
    target:`${this.packageId}::owned::new`,  
    arguments:[  
      tx.pure.address(player.toSuiAddress()),  
      tx.pure.address(opponent.toSuiAddress()),  
      tx.pure(bcs.vector(bcs.u8()).serialize(admin.toRawBytes()).toBytes()),  
],  
});  
  
  tx.transferObjects([game], admin.toSuiAddress());  
  
return tx;  
}  

```

`useTransactions.ts` also contains functions to place, send, and receive marks, end the game, and burn completed games. These functions all return a `Transaction` object, which is used in the React frontend to execute the transaction with the appropriate signer.
Click to open
`useTransactions.ts`
examples/tic-tac-toe/ui/src/hooks/useTransactions.ts
```
import{ bcs }from'@mysten/sui/bcs';  
import{PublicKey}from'@mysten/sui/cryptography';  
import{ObjectRef,Transaction}from'@mysten/sui/transactions';  
import{ useNetworkVariable }from'config';  
import{Game}from'hooks/useGameQuery';  
import{TurnCap}from'hooks/useTurnCapQuery';  
import{ multiSigPublicKey }from'MultiSig';  
  
/** Hook to provide an instance of the Transactions builder. */  
exportfunctionuseTransactions():Transactions|null{  
const packageId =useNetworkVariable('packageId');  
return packageId ?newTransactions(packageId):null;  
}  
  
/**  
 * Builds on-chain transactions for the Tic-Tac-Toe game.  
 */  
exportclassTransactions{  
readonly packageId:string;  
  
constructor(packageId:string){  
this.packageId= packageId;  
}  
  
newSharedGame(player:string, opponent:string):Transaction{  
const tx =newTransaction();  
  
		tx.moveCall({  
			target:`${this.packageId}::shared::new`,  
			arguments:[tx.pure.address(player), tx.pure.address(opponent)],  
});  
  
return tx;  
}  
  
newMultiSigGame(player:PublicKey, opponent:PublicKey):Transaction{  
const admin =multiSigPublicKey([player, opponent]);  
const tx =newTransaction();  
  
const game = tx.moveCall({  
			target:`${this.packageId}::owned::new`,  
			arguments:[  
				tx.pure.address(player.toSuiAddress()),  
				tx.pure.address(opponent.toSuiAddress()),  
				tx.pure(bcs.vector(bcs.u8()).serialize(admin.toRawBytes()).toBytes()),  
],  
});  
  
		tx.transferObjects([game], admin.toSuiAddress());  
  
return tx;  
}  
  
placeMark(game:Game, row:number, col:number):Transaction{  
if(game.kind!=='shared'){  
thrownewError('Cannot place mark directly on owned game');  
}  
  
const tx =newTransaction();  
  
		tx.moveCall({  
			target:`${this.packageId}::shared::place_mark`,  
			arguments:[tx.object(game.id), tx.pure.u8(row), tx.pure.u8(col)],  
});  
  
return tx;  
}  
  
sendMark(cap:TurnCap, row:number, col:number):Transaction{  
const tx =newTransaction();  
  
		tx.moveCall({  
			target:`${this.packageId}::owned::send_mark`,  
			arguments:[tx.object(cap.id.id), tx.pure.u8(row), tx.pure.u8(col)],  
});  
  
return tx;  
}  
  
receiveMark(game:Game, mark:ObjectRef):Transaction{  
if(game.kind!=='owned'){  
thrownewError('Cannot receive mark on shared game');  
}  
  
const tx =newTransaction();  
  
		tx.moveCall({  
			target:`${this.packageId}::owned::place_mark`,  
			arguments:[tx.object(game.id), tx.receivingRef(mark)],  
});  
  
return tx;  
}  
  
ended(game:Game):Transaction{  
const tx =newTransaction();  
  
		tx.moveCall({  
			target:`${this.packageId}::${game.kind}::ended`,  
			arguments:[tx.object(game.id)],  
});  
  
return tx;  
}  
  
burn(game:Game):Transaction{  
const tx =newTransaction();  
  
		tx.moveCall({  
			target:`${this.packageId}::${game.kind}::burn`,  
			arguments:[tx.object(game.id)],  
});  
  
return tx;  
}  
}  

```

### Placing a mark​
Placing a mark requires two transactions, just like the owned example, but they are both driven by one of the players. The first transaction is executed by the player as themselves, to send the mark to the game, and the second is executed by the player acting as the admin to place the mark they just sent. In the React frontend, this is performed as follows:
examples/tic-tac-toe/ui/src/pages/Game.tsx
```
functionOwnedGame({  
  game,  
  trophy,  
  invalidateGame,  
  invalidateTrophy,  
}:{  
  game:GameData;  
  trophy:Trophy;  
  invalidateGame:InvalidateGameQuery;  
  invalidateTrophy:InvalidateTrophyQuery;  
}):ReactElement{  
const adminKey = game.admin?newMultiSigPublicKey(newUint8Array(game.admin)):null;  
  
const client =useSuiClient();  
const signAndExecute =useExecutor();  
const multiSignAndExecute =useExecutor({  
execute:({ bytes, signature })=>{  
const multiSig = adminKey!!.combinePartialSignatures([signature]);  
return client.executeTransactionBlock({  
        transactionBlock: bytes,  
        signature:[multiSig, signature],  
        options:{  
          showRawEffects:true,  
},  
});  
},  
});  
  
const[turnCap, invalidateTurnCap]=useTurnCapQuery(game.id);  
const account =useCurrentAccount();  
const tx =useTransactions()!!;  
  
// ...  
  
constonMove=(row:number, col:number)=>{  
signAndExecute(  
{  
        tx: tx.sendMark(turnCap?.data!!, row, col),  
        options:{ showObjectChanges:true},  
},  
({ objectChanges })=>{  
const mark = objectChanges?.find(  
(c)=> c.type==='created'&& c.objectType.endsWith('::Mark'),  
);  
  
if(mark && mark.type==='created'){  
const recv = tx.receiveMark(game, mark);  
          recv.setSender(adminKey!!.toSuiAddress());  
          recv.setGasOwner(account?.address!!);  
  
multiSignAndExecute({ tx: recv },()=>{  
invalidateGame();  
invalidateTrophy();  
invalidateTurnCap();  
});  
}  
},  
);  
};  
  
// ...  
}  

```

Click to open
`Game.tsx`
examples/tic-tac-toe/ui/src/pages/Game.tsx
```
import'./Game.css';  
  
import{ useCurrentAccount, useSuiClient }from'@mysten/dapp-kit';  
import{MultiSigPublicKey}from'@mysten/sui/multisig';  
import{TrashIcon}from'@radix-ui/react-icons';  
import{AlertDialog,Badge,Button,Flex}from'@radix-ui/themes';  
import{Board}from'components/Board';  
import{Error}from'components/Error';  
import{IDLink}from'components/IDLink';  
import{Loading}from'components/Loading';  
import{GameasGameData,InvalidateGameQuery,Mark, useGameQuery }from'hooks/useGameQuery';  
import{ useTransactions }from'hooks/useTransactions';  
import{InvalidateTrophyQuery,Trophy, useTrophyQuery }from'hooks/useTrophyQuery';  
import{ useTurnCapQuery }from'hooks/useTurnCapQuery';  
import{ useExecutor }from'mutations/useExecutor';  
import{ReactElement}from'react';  
  
typeProps={  
	id:string;  
};  
  
enumTurn{  
Spectating,  
Yours,  
Theirs,  
}  
  
enumWinner{  
/** Nobody has won yet */  
None,  
  
/** X has won, and you are not a player */  
X,  
  
/** O has won, and you are not a player */  
O,  
  
/** You won */  
You,  
  
/** The other player won */  
Them,  
  
/** Game ended in a draw */  
Draw,  
}  
  
/**  
 * Render the game at the given ID.  
 *  
 * Displays the noughts and crosses board, as well as a toolbar with:  
 *  
 * - An indicator of whose turn it is.  
 * - A button to delete the game.  
 * - The ID of the game being played.  
 */  
exportdefaultfunctionGame({ id }:Props):ReactElement{  
const[game, invalidateGame]=useGameQuery(id);  
const[trophy, invalidateTrophy]=useTrophyQuery(game?.data);  
  
if(game.status==='pending'){  
return<Loading/>;  
}elseif(game.status==='error'){  
return(  
<Error title="Error loading game">  
Could not load game at <IDLink id={id} size="2" display="inline-flex"/>.  
<br />  
{game.error.message}  
</Error>  
);  
}  
  
if(trophy.status==='pending'){  
return<Loading/>;  
}elseif(trophy.status==='error'){  
return(  
<Error title="Error loading game">  
Could not check win for<IDLink id={id} size="2" display="inline-flex"/>:  
<br />  
{trophy.error.message}  
</Error>  
);  
}  
  
return game.data.kind==='shared'?(  
<SharedGame  
			game={game.data}  
			trophy={trophy.data}  
			invalidateGame={invalidateGame}  
			invalidateTrophy={invalidateTrophy}  
/>  
):(  
<OwnedGame  
			game={game.data}  
			trophy={trophy.data}  
			invalidateGame={invalidateGame}  
			invalidateTrophy={invalidateTrophy}  
/>  
);  
}  
  
functionSharedGame({  
	game,  
	trophy,  
	invalidateGame,  
	invalidateTrophy,  
}:{  
	game:GameData;  
	trophy:Trophy;  
	invalidateGame:InvalidateGameQuery;  
	invalidateTrophy:InvalidateTrophyQuery;  
}):ReactElement{  
const account =useCurrentAccount();  
const{ mutate: signAndExecute }=useExecutor();  
const tx =useTransactions()!!;  
  
const{ id, board, turn, x, o }= game;  
const[mark, curr, next]= turn %2===0?[Mark.X, x, o]:[Mark.O, o, x];  
  
// If it's the current account's turn, then empty cells should show  
// the current player's mark on hover. Otherwise show nothing, and  
// disable interactivity.  
const player =whoseTurn({ curr, next, addr: account?.address });  
const winner =whoWon({ curr, next, addr: account?.address, turn, trophy });  
const empty =Turn.Yours=== player && trophy ===Trophy.None? mark :Mark._;  
  
constonMove=(row:number, col:number)=>{  
signAndExecute({ tx: tx.placeMark(game, row, col)},()=>{  
invalidateGame();  
invalidateTrophy();  
});  
};  
  
constonDelete=(andThen:()=>void)=>{  
signAndExecute({ tx: tx.burn(game)}, andThen);  
};  
  
return(  
<>  
<Board marks={board} empty={empty} onMove={onMove}/>  
<Flex direction="row" gap="2" mx="2" my="6" justify="between">  
{trophy !==Trophy.None?(  
<WinIndicator winner={winner}/>  
):(  
<MoveIndicator turn={player}/>  
)}  
{trophy !==Trophy.None&& account ?<DeleteButton onDelete={onDelete}/>:null}  
<IDLink id={id}/>  
</Flex>  
</>  
);  
}  
  
functionOwnedGame({  
	game,  
	trophy,  
	invalidateGame,  
	invalidateTrophy,  
}:{  
	game:GameData;  
	trophy:Trophy;  
	invalidateGame:InvalidateGameQuery;  
	invalidateTrophy:InvalidateTrophyQuery;  
}):ReactElement{  
const adminKey = game.admin?newMultiSigPublicKey(newUint8Array(game.admin)):null;  
  
const client =useSuiClient();  
const{ mutate: signAndExecute }=useExecutor();  
const{ mutate: multiSignAndExecute }=useExecutor({  
execute:({ bytes, signature })=>{  
// SAFETY: We check below whether the admin key is available,  
// and only allow moves to be submitted when it is.  
const multiSig = adminKey!!.combinePartialSignatures([signature]);  
return client.executeTransactionBlock({  
				transactionBlock: bytes,  
// The multi-sig authorizes access to the game object, while  
// the original signature authorizes access to the player's  
// gas object, because the player is sponsoring the  
// transaction.  
				signature:[multiSig, signature],  
				options:{  
					showRawEffects:true,  
},  
});  
},  
});  
  
const[turnCap, invalidateTurnCap]=useTurnCapQuery(game.id);  
const account =useCurrentAccount();  
const tx =useTransactions()!!;  
  
if(adminKey ==null){  
return(  
<Error title="Error loading game">  
Could not load game at <IDLink id={game.id} size="2" display="inline-flex"/>.  
<br />  
Game has no admin.  
</Error>  
);  
}  
  
if(turnCap.status==='pending'){  
return<Loading/>;  
}elseif(turnCap.status==='error'){  
return(  
<Error title="Error loading game">  
Could not load turn capability.  
<br />  
{turnCap.error?.message}  
</Error>  
);  
}  
  
const{ id, board, turn, x, o }= game;  
const[mark, curr, next]= turn %2===0?[Mark.X, x, o]:[Mark.O, o, x];  
  
// If it's the current account's turn, then empty cells should show  
// the current player's mark on hover. Otherwise show nothing, and  
// disable interactivity.  
const player =whoseTurn({ curr, next, addr: account?.address });  
const winner =whoWon({ curr, next, addr: account?.address, turn, trophy });  
const empty =Turn.Yours=== player && trophy ===Trophy.None? mark :Mark._;  
  
constonMove=(row:number, col:number)=>{  
signAndExecute(  
{  
// SAFETY: TurnCap should only be unavailable if the game is over.  
				tx: tx.sendMark(turnCap?.data!!, row, col),  
				options:{ showObjectChanges:true},  
},  
({ objectChanges })=>{  
const mark = objectChanges?.find(  
(c)=> c.type==='created'&& c.objectType.endsWith('::Mark'),  
);  
  
if(mark && mark.type==='created'){  
// SAFETY: UI displays error if the admin key is not  
// available, and interactivity is disabled if there is not a  
// valid account.  
//  
// The transaction to make the actual move is made by the  
// multi-sig account (which owns the game), and is sponsored  
// by the player (as the multi-sig account doesn't have coins  
// of its own).  
const recv = tx.receiveMark(game, mark);  
					recv.setSender(adminKey!!.toSuiAddress());  
					recv.setGasOwner(account?.address!!);  
  
multiSignAndExecute({ tx: recv },()=>{  
invalidateGame();  
invalidateTrophy();  
invalidateTurnCap();  
});  
}  
},  
);  
};  
  
constonDelete=(andThen:()=>void)=>{  
// Just like with making a move, deletion has to be implemented as  
// a sponsored multi-sig transaction. This means only one of the  
// two players can clean up a finished game.  
const burn = tx.burn(game);  
		burn.setSender(adminKey!!.toSuiAddress());  
		burn.setGasOwner(account?.address!!);  
  
multiSignAndExecute({ tx: burn }, andThen);  
};  
  
return(  
<>  
<Board marks={board} empty={empty} onMove={onMove}/>  
<Flex direction="row" gap="2" mx="2" my="6" justify="between">  
{trophy !==Trophy.None?(  
<WinIndicator winner={winner}/>  
):(  
<MoveIndicator turn={player}/>  
)}  
{trophy !==Trophy.None&& player !==Turn.Spectating?(  
<DeleteButton onDelete={onDelete}/>  
):null}  
<IDLink id={id}/>  
</Flex>  
</>  
);  
}  
  
/**  
 * Figure out whose turn it should be based on who the `curr`ent  
 * player is, who the `next` player is, and what the `addr`ess of the  
 * current account is.  
 */  
functionwhoseTurn({ curr, next, addr }:{ curr:string; next:string; addr?:string}):Turn{  
if(addr === curr){  
returnTurn.Yours;  
}elseif(addr === next){  
returnTurn.Theirs;  
}else{  
returnTurn.Spectating;  
}  
}  
  
/**  
 * Figure out who won the game, out of the `curr`ent, and `next`  
 * players, relative to whose asking (`addr`). `turns` indicates the  
 * number of turns we've seen so far, which is used to determine which  
 * address corresponds to player X and player O.  
 */  
functionwhoWon({  
	curr,  
	next,  
	addr,  
	turn,  
	trophy,  
}:{  
	curr:string;  
	next:string;  
	addr?:string;  
	turn:number;  
	trophy:Trophy;  
}):Winner{  
switch(trophy){  
caseTrophy.None:  
returnWinner.None;  
caseTrophy.Draw:  
returnWinner.Draw;  
caseTrophy.Win:  
// These tests are "backwards" because the game advances to the  
// next turn after the win has happened. Nevertheless, make sure  
// to test for the "you" case before the "them" case to handle a  
// situation where a player is playing themselves.  
if(addr === next){  
returnWinner.You;  
}elseif(addr === curr){  
returnWinner.Them;  
}elseif(turn %2===0){  
returnWinner.O;  
}else{  
returnWinner.X;  
}  
}  
}  
  
functionMoveIndicator({ turn }:{ turn:Turn}):ReactElement{  
switch(turn){  
caseTurn.Yours:  
return<Badge color="green">Your turn</Badge>;  
caseTurn.Theirs:  
return<Badge color="orange">Their turn</Badge>;  
caseTurn.Spectating:  
return<Badge color="blue">Spectating</Badge>;  
}  
}  
  
functionWinIndicator({ winner }:{ winner:Winner}):ReactElement|null{  
switch(winner){  
caseWinner.None:  
returnnull;  
caseWinner.Draw:  
return<Badge color="orange">Draw!</Badge>;  
caseWinner.You:  
return<Badge color="green">YouWin!</Badge>;  
caseWinner.Them:  
return<Badge color="red">YouLose!</Badge>;  
caseWinner.X:  
return<Badge color="blue">XWins!</Badge>;  
caseWinner.O:  
return<Badge color="blue">OWins!</Badge>;  
}  
}  
  
/**  
 * "Delete" button with a confirmation dialog. On confirmation, the  
 * button calls `onDelete`, passing in an action to perform after  
 * deletion has completed (returning to the homepage).  
 */  
functionDeleteButton({ onDelete }:{onDelete:(andThen:()=>void)=>void}):ReactElement{  
constredirect=()=>{  
// Navigate back to homepage, because the game is gone now.  
window.location.href='/';  
};  
  
return(  
<AlertDialog.Root>  
<AlertDialog.Trigger>  
<Button color="red" size="1" variant="outline">  
<TrashIcon/>DeleteGame  
</Button>  
</AlertDialog.Trigger>  
<AlertDialog.Content>  
<AlertDialog.Title>DeleteGame</AlertDialog.Title>  
<AlertDialog.Description>  
Are you sure you want to deletethis game?This will delete the object from the blockchain  
					and cannot be undone.  
</AlertDialog.Description>  
<Flex gap="3" mt="3" justify="end">  
<AlertDialog.Cancel>  
<Button variant="soft" color="gray">  
Cancel  
</Button>  
</AlertDialog.Cancel>  
<AlertDialog.Action onClick={()=>onDelete(redirect)}>  
<Button variant="solid" color="red">  
Delete  
</Button>  
</AlertDialog.Action>  
</Flex>  
</AlertDialog.Content>  
</AlertDialog.Root>  
);  
}  

```

The first step is to get the multisig public key, which was written to `Game.admin` earlier. Then two executor hooks are created: The first is to sign and execute as the current player, and the second is to sign and execute as the multisig/admin account. After the wallet has serialized and signed the transaction the second executor creates a multisig from the wallet signature and executes the transaction with two signatures: Authorizing on behalf of the multisig and the wallet.
The reason for the two signatures is clearer when looking at the construction of the `recv` transaction: The multisig authorizes access to the `Game`, and the wallet authorizes access to the gas object. This is because the multisig account does not hold any coins of its own, so it relies on the player account to sponsor the transaction.
You can find an example React front-end supporting both the multi-sig and shared variants of the game in the ui directory, and a CLI written in Rust in the cli directory.
Previous
Plinko
Next
Oracles
  * What the guide teaches
  * What you need
  * Directory structure
  * owned.move
  * shared.move
  * Multisig
    * Creating a multisig account
    * Building a multisig transaction
    * Placing a mark


![Sui Logo](https://docs.sui.io/img/sui-logo-footer.svg)
© 2025 Sui Foundation | Documentation distributed under CC BY 4.0
